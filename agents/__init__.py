# agents/__init__.py
"""
Agent package - AI agents for TaskFlow system
"""

# Import base classes
from .base_agent import (
    BaseAgent,
    AgentRegistry,
    agent_registry,
    register_agent,
    get_agent,
)

# Import specific agents when their modules are available
try:
    from .system_organizer import SystemOrganizerAgent, create_system_organizer
except ImportError:
    pass  # Module might not be ready yet

__all__ = [
    "BaseAgent",
    "AgentRegistry",
    "agent_registry",
    "register_agent",
    "get_agent",
    "SystemOrganizerAgent",
    "create_system_organizer",
]
