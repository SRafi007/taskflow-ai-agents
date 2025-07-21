from agents.base_agent import BaseAgent
from tools import get_tool
from models.local_llm import LocalLLM
from config.settings import get_model_config


class WebIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Web Intelligence",
            role="Web Intelligence Analyst",
            description="Monitors news, tracks prices, and gathers live web information.",
            personality="Curious, data-driven, and alert.",
            tools=["WebSearchTool"],
        )
        model_config = get_model_config()
        self.llm = LocalLLM(
            model_name=model_config["model_name"], base_url=model_config["base_url"]
        )

    def execute_task(self, task_description, inputs=None):
        self.clear_history()
        self.add_to_history("user", task_description)

        tool = get_tool("WebSearchTool")
        if not tool:
            return {"success": False, "error": "WebSearchTool not registered"}

        search_term = inputs.get("query") if inputs else task_description
        result = tool.execute(query=search_term)

        if result["success"]:
            result_str = "\n".join(
                [f"- {r['title']}: {r['link']}" for r in result["result"]]
            )
            full_prompt = f"Summarize the following web results for '{search_term}':\n\n{result_str}"
            self.add_to_history("system", full_prompt)
            response = self.llm.generate(full_prompt)
            self.add_to_history("assistant", response)
            return {"success": True, "result": response}
        else:
            return result
