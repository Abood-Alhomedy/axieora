from typing import Callable, Dict, Any, List
from pydantic import BaseModel

class ToolConfig(BaseModel):
    id: str
    name: str
    description: str
    parameters: Dict[str, Any]

class ToolRegistry:
    _tools: Dict[str, dict] = {}

    @classmethod
    def register(cls, config: ToolConfig, executor: Callable):
        cls._tools[config.id] = {"config": config, "executor": executor}

    @classmethod
    def get_tool(cls, tool_id: str):
        return cls._tools.get(tool_id)

    @classmethod
    def get_all_llm_schemas(cls) -> List[Dict]:
        schemas = []
        for tool in cls._tools.values():
            config = tool["config"]
            schemas.append({
                "type": "function",
                "function": {
                    "name": config.id,
                    "description": config.description,
                    "parameters": config.parameters
                }
            })
        return schemas