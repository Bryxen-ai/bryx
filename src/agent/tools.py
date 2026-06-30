# from pydantic import BaseModel
from dataclasses import dataclass
from typing import Callable, Any

"""
class ToolDef

class ToolRegistry
    def __init__(self):
        self._tools = dict[str, ToolDef] = {}
    
    def register(self, tool: ToolDef): -> None
        self._tools[tool.schema['name']] = tool
        
    def schema(self): -> list[dict]
        return [i.schema for i in self._tools]
    
    async def dispatch(self,name,input_: dict): -> str
        tool = self._tools.get(name)
        if tool is None:
            return Error
        try:
            return await tool.handler(input_)
        except:
            ERROR
    
    def names(self): -> str
        return list(self._tools.keys())

---
Tool Sample: READ

async _now_handler(inp:dict)
    await asyncio.sleep(0)
    return datetime.now().isoformat()
    
NOW_SCHEMA = {
    "name": "now",
    "description": "get current date and time",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
    
}

registry.register(ToolDef(schema=NOW_SCHEMA, handler=_now_handler))

"""



@dataclass
class ToolDef:
    schema: dict
    handler: Callable[..., Any]
    

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDef] = {}
    
    def register(self, tool:ToolDef) -> None:
        self._tools[tool.schema["name"]] = tool
    
    def schemas(self):
        return [i.schema for i in self._tools.valuse]

    async def dispatch(self, name:str, _inp: dict) -> str:
        tool = self._tools.get(name)
        if tool is None:
            return "ERROR: tool is None"
        
        try:
            return await tool.handler(_inp)
        except Exception as e:
            return f"Error: {e}"
        
    def names(self) -> list[str]:
        return self._tools.keys()



if __name__ == "__main__":
    import asyncio
    from datetime import datetime
    
    NOW_SCHEMA = {
    "name": "now",
    "description": "get current date and time",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
        }   
    
    }
    
    async def _now_handler(inp:dict):
        await asyncio.sleep(0)
        print(inp.get("description"))
        return datetime.now().isoformat()
    
    registry = ToolRegistry()
    
    registry.register(
        ToolDef(
            schema=NOW_SCHEMA,
            handler=_now_handler
        )
    )
    
    result = asyncio.run(registry.dispatch(name="now",_inp=NOW_SCHEMA))
    print(result)