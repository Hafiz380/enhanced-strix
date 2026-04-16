import asyncio
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any

import litellm
from jinja2 import Environment, FileSystemLoader, select_autoescape
from litellm import acompletion, completion_cost, stream_chunk_builder, supports_reasoning
from litellm.utils import supports_prompt_caching, supports_vision

from strix.config import Config
from strix.config.settings_manager import SettingsManager
from strix.llm.cache import LLMCache
from strix.llm.config import LLMConfig
from strix.telemetry.token_report import TokenReporter
from strix.llm.memory_compressor import MemoryCompressor
from strix.llm.utils import (
    _truncate_to_first_function,
    fix_incomplete_tool_call,
    normalize_tool_format,
    parse_tool_invocations,
)
from strix.skills import load_skills
from strix.tools import get_tools_prompt
from strix.utils.resource_paths import get_strix_resource_path


litellm.drop_params = True
litellm.modify_params = True


class LLMRequestFailedError(Exception):
    def __init__(self, message: str, details: str | None = None):
        super().__init__(message)
        self.message = message
        self.details = details


@dataclass
class LLMResponse:
    content: str
    tool_invocations: list[dict[str, Any]] | None = None
    thinking_blocks: list[dict[str, Any]] | None = None


@dataclass
class RequestStats:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    cost: float = 0.0
    requests: int = 0

    def to_dict(self) -> dict[str, int | float]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cached_tokens": self.cached_tokens,
            "cost": round(self.cost, 4),
            "requests": self.requests,
        }


class LLM:
    def __init__(self, config: LLMConfig, agent_name: str | None = None):
        self.config = config
        self.agent_name = agent_name
        self.agent_id: str | None = None
        self._active_skills: list[str] = list(config.skills or [])
        self._system_prompt_context: dict[str, Any] = dict(
            getattr(config, "system_prompt_context", {}) or {}
        )
        self._total_stats = RequestStats()
        self.cache = LLMCache()
        self.settings_manager = SettingsManager()
        self.token_reporter = TokenReporter()
        self.memory_compressor = MemoryCompressor(model_name=config.litellm_model)
        self.system_prompt = self._load_system_prompt(agent_name)

        reasoning = Config.get("strix_reasoning_effort")
        if reasoning:
            self._reasoning_effort = reasoning
        elif config.reasoning_effort:
            self._reasoning_effort = config.reasoning_effort
        elif config.scan_mode == "quick":
            self._reasoning_effort = "medium"
        else:
            self._reasoning_effort = "high"

    def _load_system_prompt(self, agent_name: str | None) -> str:
        if not agent_name:
            return ""

        try:
            prompt_dir = get_strix_resource_path("agents", agent_name)
            skills_dir = get_strix_resource_path("skills")
            env = Environment(
                loader=FileSystemLoader([prompt_dir, skills_dir]),
                autoescape=select_autoescape(enabled_extensions=(), default_for_string=False),
            )

            skills_to_load = self._get_skills_to_load()
            skill_content = load_skills(skills_to_load)
            env.globals["get_skill"] = lambda name: skill_content.get(name, "")

            result = env.get_template("system_prompt.jinja").render(
                get_tools_prompt=get_tools_prompt,
                loaded_skill_names=list(skill_content.keys()),
                interactive=self.config.interactive,
                system_prompt_context=self._system_prompt_context,
                ecc_rules=self._system_prompt_context.get("ecc_rules"),
                ecc_persona=self._system_prompt_context.get("ecc_persona"),
                **skill_content,
            )
            return str(result)
        except Exception:  # noqa: BLE001
            return ""

    def _get_skills_to_load(self) -> list[str]:
        ordered_skills = [*self._active_skills]
        ordered_skills.append(f"scan_modes/{self.config.scan_mode}")
        if self.config.is_whitebox:
            ordered_skills.append("coordination/source_aware_whitebox")
            ordered_skills.append("custom/source_aware_sast")

        deduped: list[str] = []
        seen: set[str] = set()
        for skill_name in ordered_skills:
            if skill_name not in seen:
                deduped.append(skill_name)
                seen.add(skill_name)

        return deduped

    def add_skills(self, skill_names: list[str]) -> list[str]:
        added: list[str] = []
        for skill_name in skill_names:
            if not skill_name or skill_name in self._active_skills:
                continue
            self._active_skills.append(skill_name)
            added.append(skill_name)

        if not added:
            return []

        updated_prompt = self._load_system_prompt(self.agent_name)
        if updated_prompt:
            self.system_prompt = updated_prompt

        return added

    def set_agent_identity(self, agent_name: str | None, agent_id: str | None) -> None:
        if agent_name:
            self.agent_name = agent_name
        if agent_id:
            self.agent_id = agent_id

    def set_system_prompt_context(self, context: dict[str, Any] | None) -> None:
        self._system_prompt_context = dict(context or {})
        updated_prompt = self._load_system_prompt(self.agent_name)
        if updated_prompt:
            self.system_prompt = updated_prompt

    async def generate(
        self, conversation_history: list[dict[str, Any]]
    ) -> AsyncIterator[LLMResponse]:
        messages = self._prepare_messages(conversation_history)
        
        # Check cache first
        cached_response = self.cache.get(messages, self.config.litellm_model)
        if cached_response:
            self._total_stats.requests += 1
            self._total_stats.cached_tokens += cached_response.get("usage", {}).get("prompt_tokens", 0)
            yield LLMResponse(
                content=cached_response["content"],
                tool_invocations=cached_response.get("tool_invocations"),
                thinking_blocks=cached_response.get("thinking_blocks"),
            )
            return

        max_retries = int(Config.get("strix_llm_max_retries") or "5")

        for attempt in range(max_retries + 1):
            # Select best API config if failover is needed or if none is provided
            api_cfg = self.settings_manager.get_best_config()
            start_time = time.time()
            
            try:
                accumulated_content = ""
                async for response in self._stream(messages, api_cfg):
                    accumulated_content = response.content
                    yield response
                
                # Update performance stats on success
                if api_cfg:
                    latency = time.time() - start_time
                    self.settings_manager.update_performance(api_cfg.name, latency, success=True)
                
                # Cache the successful result
                # (We'll need to store the final response with usage info)
                # This is done inside _stream's last yield or after _stream ends
                return 
            except Exception as e:
                # Update performance stats on failure
                if api_cfg:
                    self.settings_manager.update_performance(api_cfg.name, 0, success=False)
                
                if attempt >= max_retries or not self._should_retry(e):
                    self._raise_error(e)
                wait = min(90, 2 * (2**attempt))
                await asyncio.sleep(wait)

    async def _stream(self, messages: list[dict[str, Any]], api_cfg: Optional[Any] = None) -> AsyncIterator[LLMResponse]:
        accumulated = ""
        chunks: list[Any] = []
        done_streaming = 0

        self._total_stats.requests += 1
        completion_args = self._build_completion_args(messages, api_cfg)
        response = await acompletion(**completion_args, stream=True)

        async for chunk in response:
            chunks.append(chunk)
            if done_streaming:
                done_streaming += 1
                if getattr(chunk, "usage", None) or done_streaming > 5:
                    break
                continue
            delta = self._get_chunk_content(chunk)
            if delta:
                accumulated += delta
                if "</function>" in accumulated or "</invoke>" in accumulated:
                    end_tag = "</function>" if "</function>" in accumulated else "</invoke>"
                    pos = accumulated.find(end_tag)
                    accumulated = accumulated[: pos + len(end_tag)]
                    yield LLMResponse(content=accumulated)
                    done_streaming = 1
                    continue
                yield LLMResponse(content=accumulated)

        if chunks:
            response_obj = stream_chunk_builder(chunks)
            self._update_usage_stats(response_obj)
            
            # Cache the final result
            self.cache.set(
                messages, 
                self.config.litellm_model, 
                {
                    "content": accumulated,
                    "tool_invocations": parse_tool_invocations(accumulated),
                    "thinking_blocks": self._extract_thinking(chunks),
                    "usage": getattr(response_obj, "usage", {}).to_dict() if hasattr(response_obj, "usage") and response_obj.usage else {}
                }
            )

        accumulated = normalize_tool_format(accumulated)
        accumulated = fix_incomplete_tool_call(_truncate_to_first_function(accumulated))
        yield LLMResponse(
            content=accumulated,
            tool_invocations=parse_tool_invocations(accumulated),
            thinking_blocks=self._extract_thinking(chunks),
        )

    def _prepare_messages(self, conversation_history: list[dict[str, Any]]) -> list[dict[str, Any]]:
        messages = [{"role": "system", "content": self.system_prompt}]

        if self.agent_name:
            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"\n\n<agent_identity>\n"
                        f"<meta>Internal metadata: do not echo or reference.</meta>\n"
                        f"<agent_name>{self.agent_name}</agent_name>\n"
                        f"<agent_id>{self.agent_id}</agent_id>\n"
                        f"</agent_identity>\n\n"
                    ),
                }
            )

        compressed = list(self.memory_compressor.compress_history(conversation_history))
        conversation_history.clear()
        conversation_history.extend(compressed)
        messages.extend(compressed)

        if messages[-1].get("role") == "assistant" and not self.config.interactive:
            messages.append({"role": "user", "content": "<meta>Continue the task.</meta>"})

        if self._is_anthropic() and self.config.enable_prompt_caching:
            messages = self._add_cache_control(messages)

        return messages

    def _build_completion_args(self, messages: list[dict[str, Any]], api_cfg: Optional[Any] = None) -> dict[str, Any]:
        if not self._supports_vision():
            messages = self._strip_images(messages)

        model = self.config.litellm_model
        api_key = self.config.api_key
        api_base = self.config.api_base

        if api_cfg:
            model = api_cfg.model
            api_key = api_cfg.api_key
            api_base = api_cfg.api_base

        args: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "timeout": self.config.timeout,
            "stream_options": {"include_usage": True},
        }

        if api_key:
            args["api_key"] = api_key
        if api_base:
            args["api_base"] = api_base
        if self._supports_reasoning():
            args["reasoning_effort"] = self._reasoning_effort

        return args

    def _get_chunk_content(self, chunk: Any) -> str:
        if chunk.choices and hasattr(chunk.choices[0], "delta"):
            return getattr(chunk.choices[0].delta, "content", "") or ""
        return ""

    def _extract_thinking(self, chunks: list[Any]) -> list[dict[str, Any]] | None:
        if not chunks or not self._supports_reasoning():
            return None
        try:
            resp = stream_chunk_builder(chunks)
            if resp.choices and hasattr(resp.choices[0].message, "thinking_blocks"):
                blocks: list[dict[str, Any]] = resp.choices[0].message.thinking_blocks
                return blocks
        except Exception:  # noqa: BLE001, S110  # nosec B110
            pass
        return None

    def _update_usage_stats(self, response: Any) -> None:
        try:
            if hasattr(response, "usage") and response.usage:
                input_tokens = getattr(response.usage, "prompt_tokens", 0) or 0
                output_tokens = getattr(response.usage, "completion_tokens", 0) or 0

                cached_tokens = 0
                if hasattr(response.usage, "prompt_tokens_details"):
                    prompt_details = response.usage.prompt_tokens_details
                    if hasattr(prompt_details, "cached_tokens"):
                        cached_tokens = prompt_details.cached_tokens or 0

                cost = self._extract_cost(response)
            else:
                input_tokens = 0
                output_tokens = 0
                cached_tokens = 0
                cost = 0.0

            self._total_stats.input_tokens += input_tokens
            self._total_stats.output_tokens += output_tokens
            self._total_stats.cached_tokens += cached_tokens
            self._total_stats.cost += cost

        except Exception:  # noqa: BLE001, S110  # nosec B110
            pass

    def _extract_cost(self, response: Any) -> float:
        if hasattr(response, "usage") and response.usage:
            direct_cost = getattr(response.usage, "cost", None)
            if direct_cost is not None:
                return float(direct_cost)
        try:
            if hasattr(response, "_hidden_params"):
                response._hidden_params.pop("custom_llm_provider", None)
            return completion_cost(response, model=self.config.canonical_model) or 0.0
        except Exception:  # noqa: BLE001
            return 0.0

    def _should_retry(self, e: Exception) -> bool:
        code = getattr(e, "status_code", None) or getattr(
            getattr(e, "response", None), "status_code", None
        )
        return code is None or litellm._should_retry(code)

    def _raise_error(self, e: Exception) -> None:
        from strix.telemetry import posthog

        posthog.error("llm_error", type(e).__name__)
        raise LLMRequestFailedError(f"LLM request failed: {type(e).__name__}", str(e)) from e

    def _is_anthropic(self) -> bool:
        if not self.config.model_name:
            return False
        return any(p in self.config.model_name.lower() for p in ["anthropic/", "claude"])

    def _supports_vision(self) -> bool:
        try:
            return bool(supports_vision(model=self.config.canonical_model))
        except Exception:  # noqa: BLE001
            return False

    def _supports_reasoning(self) -> bool:
        try:
            return bool(supports_reasoning(model=self.config.canonical_model))
        except Exception:  # noqa: BLE001
            return False

    def _strip_images(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = []
        for msg in messages:
            content = msg.get("content")
            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                    elif isinstance(item, dict) and item.get("type") == "image_url":
                        text_parts.append("[Image removed - model doesn't support vision]")
                result.append({**msg, "content": "\n".join(text_parts)})
            else:
                result.append(msg)
        return result

    def _add_cache_control(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not messages or not supports_prompt_caching(self.config.canonical_model):
            return messages

        result = list(messages)

        if result[0].get("role") == "system":
            content = result[0]["content"]
            result[0] = {
                **result[0],
                "content": [
                    {"type": "text", "text": content, "cache_control": {"type": "ephemeral"}}
                ]
                if isinstance(content, str)
                else content,
            }
        return result
