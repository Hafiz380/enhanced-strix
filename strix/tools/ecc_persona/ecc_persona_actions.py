import os
from typing import Any
from strix.tools.registry import register_tool
from strix.utils.resource_paths import get_strix_resource_path

@register_tool(sandbox_execution=False)
def load_ecc_persona(agent_state: Any, persona_name: str) -> dict[str, Any]:
    """
    Switch the current agent's persona to an ECC specialized persona.
    Available personas are located in strix/agents/ecc_personas/.
    """
    try:
        persona_dir = get_strix_resource_path("agents", "ecc_personas")
        persona_file = os.path.join(persona_dir, f"{persona_name}.md")
        
        if not os.path.exists(persona_file):
            available_personas = [f.replace(".md", "") for f in os.listdir(persona_dir) if f.endswith(".md")]
            return {
                "success": False,
                "error": f"Persona '{persona_name}' not found. Available personas: {', '.join(available_personas)}",
            }
            
        with open(persona_file, 'r', encoding='utf-8') as f:
            persona_content = f.read()
            
        from strix.tools.agents_graph.agents_graph_actions import _agent_instances
        current_agent = _agent_instances.get(agent_state.agent_id)
        
        if current_agent is None or not hasattr(current_agent, "llm"):
            return {
                "success": False,
                "error": "Could not find running agent instance to update persona.",
            }
            
        # Update system prompt context with the new persona
        new_context = dict(current_agent.llm._system_prompt_context)
        new_context["ecc_persona"] = {
            "name": persona_name,
            "description": persona_content[:200] + "..." # Brief description from file
        }
        
        current_agent.llm.set_system_prompt_context(new_context)
        agent_state.update_context("active_ecc_persona", persona_name)
        
        return {
            "success": True,
            "persona_name": persona_name,
            "message": f"Agent persona successfully switched to '{persona_name}'.",
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to load ECC persona: {e!s}",
        }
