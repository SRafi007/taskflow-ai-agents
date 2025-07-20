# tools/base_tool.py
"""
Base tool interface - Simple foundation for all agent tools
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseTool(ABC):
    """
    Simple base class for all agent tools
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.enabled = True

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters

        Returns:
            Dict with 'success', 'result', and optional 'error' keys
        """
        pass

    def is_available(self) -> bool:
        """Check if tool can be used (permissions, dependencies, etc.)"""
        return self.enabled

    def get_info(self) -> Dict[str, str]:
        """Get basic info about this tool"""
        return {
            "name": self.name,
            "description": self.description,
            "available": str(self.is_available()),
        }


class ToolRegistry:
    """
    Simple registry to keep track of available tools
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        """Register a tool by its name"""
        self._tools[tool.name] = tool
        print(f"🔧 Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self._tools.get(name)

    def list_tools(self) -> Dict[str, BaseTool]:
        """Get all registered tools"""
        return self._tools.copy()


# Global tool registry instance
tool_registry = ToolRegistry()


def register_tool(tool: BaseTool):
    """Convenience function to register a tool"""
    tool_registry.register(tool)


def get_tool(name: str) -> Optional[BaseTool]:
    """Convenience function to get a tool"""
    return tool_registry.get_tool(name)
