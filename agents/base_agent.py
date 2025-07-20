# agents/base_agent.py
"""
Base agent class - Foundation for all AI agents
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Simple base class for all AI agents
    """

    def __init__(
        self,
        name: str,
        role: str,
        description: str,
        personality: str = "",
        tools: List[str] = None,
    ):
        self.name = name
        self.role = role
        self.description = description
        self.personality = personality
        self.tools = tools or []
        self.conversation_history = []

    @abstractmethod
    def execute_task(
        self, task_description: str, inputs: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Execute a task and return results

        Args:
            task_description: What the agent should do
            inputs: Any input data needed for the task

        Returns:
            Dict with 'success', 'result', and optional 'error' keys
        """
        pass

    def get_system_prompt(self) -> str:
        """Build the system prompt for this agent"""
        prompt_parts = [
            f"You are {self.name}, a {self.role}.",
            f"Description: {self.description}",
        ]

        if self.personality:
            prompt_parts.append(f"Personality: {self.personality}")

        if self.tools:
            prompt_parts.append(f"Available tools: {', '.join(self.tools)}")

        return "\n\n".join(prompt_parts)

    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_info(self) -> Dict[str, Any]:
        """Get basic information about this agent"""
        return {
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "tools": self.tools,
            "history_length": len(self.conversation_history),
        }


class AgentRegistry:
    """
    Simple registry to manage available agents
    """

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent):
        """Register an agent"""
        self._agents[agent.name] = agent
        print(f"🤖 Registered agent: {agent.name}")

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get agent by name"""
        return self._agents.get(name)

    def list_agents(self) -> Dict[str, BaseAgent]:
        """Get all registered agents"""
        return self._agents.copy()


# Global agent registry
agent_registry = AgentRegistry()


def register_agent(agent: BaseAgent):
    """Convenience function to register an agent"""
    agent_registry.register(agent)


def get_agent(name: str) -> Optional[BaseAgent]:
    """Convenience function to get an agent"""
    return agent_registry.get_agent(name)
