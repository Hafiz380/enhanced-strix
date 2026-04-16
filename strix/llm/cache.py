import hashlib
import json
import os
from pathlib import Path
from typing import Any, Optional


class LLMCache:
    """Caching mechanism for LLM responses to save tokens and reduce API calls."""

    def __init__(self, cache_dir: Optional[Path] = None):
        if cache_dir is None:
            self.cache_dir = Path.home() / ".strix" / "cache"
        else:
            self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, messages: list[dict[str, Any]], model: str, **kwargs: Any) -> str:
        """Generate a unique hash for the request."""
        # Normalize messages to avoid cache misses due to key order
        msg_str = json.dumps(messages, sort_keys=True)
        kwargs_str = json.dumps(kwargs, sort_keys=True)
        combined = f"{model}:{msg_str}:{kwargs_str}"
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def get(self, messages: list[dict[str, Any]], model: str, **kwargs: Any) -> Optional[dict[str, Any]]:
        """Retrieve a cached response if it exists."""
        key = self._get_cache_key(messages, model, **kwargs)
        cache_file = self.cache_dir / f"{key}.json"
        
        if cache_file.exists():
            try:
                with cache_file.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return None
        return None

    def set(self, messages: list[dict[str, Any]], model: str, response: dict[str, Any], **kwargs: Any) -> None:
        """Store a response in the cache."""
        key = self._get_cache_key(messages, model, **kwargs)
        cache_file = self.cache_dir / f"{key}.json"
        
        try:
            with cache_file.open("w", encoding="utf-8") as f:
                json.dump(response, f, indent=2)
        except OSError:
            pass
