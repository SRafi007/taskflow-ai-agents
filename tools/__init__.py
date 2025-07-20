# tools/__init__.py
"""
Tools package - External capabilities for agents
"""

# Import base classes
from .base_tool import BaseTool, ToolRegistry, tool_registry, register_tool, get_tool

# Import specific tools when available
try:
    from .file_organizer import FileOrganizerTool, file_organizer_tool
except ImportError:
    pass  # Module might not be ready yet

__all__ = [
    "BaseTool",
    "ToolRegistry",
    "tool_registry",
    "register_tool",
    "get_tool",
    "FileOrganizerTool",
    "file_organizer_tool",
]
