# agents/system_organizer.py
"""
System Organizer Agent - Manages files and folder organization
"""

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent, register_agent
from tools.base_tool import get_tool
from models.local_llm import LocalLLM


class SystemOrganizerAgent(BaseAgent):
    """
    Agent specialized in file and folder organization tasks
    """

    def __init__(self, llm: LocalLLM = None):
        super().__init__(
            name="System Organizer",
            role="organizer",
            description="Manages files, folders, and system organization tasks",
            personality="You are a meticulous system organizer who keeps everything neat and efficient.",
            tools=["file_organizer"],
        )
        self.llm = llm or LocalLLM()

    def execute_task(
        self, task_description: str, inputs: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Execute file organization task
        """
        inputs = inputs or {}

        try:
            # Build the prompt for the LLM
            system_prompt = self.get_system_prompt()

            # Add task-specific context
            user_prompt = f"""
Task: {task_description}

Inputs: {json.dumps(inputs, indent=2)}

Available actions with file_organizer tool:
1. 'analyze' - Analyze folder structure (needs: folder_path)
2. 'organize' - Organize files by type (needs: folder_path)  
3. 'create_folders' - Create folder structure (needs: folder_path, folders list)

Please decide what action to take and provide the parameters in this JSON format:
{{
    "action": "action_name",
    "parameters": {{
        "param1": "value1",
        "param2": "value2"
    }}
}}

Only respond with the JSON, no other text.
"""

            # Get decision from LLM
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            llm_response = self.llm.chat(messages, max_tokens=300, temperature=0.2)

            # Parse LLM response to get action and parameters
            try:
                # Extract JSON from response (in case there's extra text)
                json_start = llm_response.find("{")
                json_end = llm_response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = llm_response[json_start:json_end]
                    decision = json.loads(json_str)
                else:
                    return {
                        "success": False,
                        "error": "Could not parse LLM response as JSON",
                    }

            except json.JSONDecodeError as e:
                return {"success": False, "error": f"Invalid JSON from LLM: {e}"}

            # Execute the decided action using the file_organizer tool
            tool = get_tool("file_organizer")
            if not tool:
                return {"success": False, "error": "file_organizer tool not available"}

            action = decision.get("action")
            parameters = decision.get("parameters", {})

            result = tool.execute(action=action, **parameters)

            # Add to conversation history
            self.add_to_history("user", task_description)
            self.add_to_history("assistant", f"Executed {action} with result: {result}")

            return {
                "success": result.get("success", False),
                "result": result.get("result"),
                "error": result.get("error"),
                "action_taken": action,
                "parameters_used": parameters,
            }

        except Exception as e:
            return {"success": False, "error": f"Agent execution failed: {str(e)}"}

    def analyze_folder(self, folder_path: str) -> Dict[str, Any]:
        """Convenience method to analyze a folder"""
        return self.execute_task(
            f"Analyze the folder structure at {folder_path}",
            {"folder_path": folder_path},
        )

    def organize_folder(self, folder_path: str) -> Dict[str, Any]:
        """Convenience method to organize a folder"""
        return self.execute_task(
            f"Organize files in {folder_path} by type", {"folder_path": folder_path}
        )


# Register the agent when module is imported
def create_system_organizer(llm: LocalLLM = None) -> SystemOrganizerAgent:
    """Factory function to create and register system organizer agent"""
    agent = SystemOrganizerAgent(llm)
    register_agent(agent)
    return agent
