from tools.base_tool import BaseTool
import requests
from typing import Dict, Any
import os


class WebSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="WebSearchTool",
            description="Searches the web using a custom search engine",
        )
        self.api_key = os.getenv("GOOGLE_API_KEY", "")
        self.search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")

    def execute(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        if not self.api_key or not self.search_engine_id:
            return {"success": False, "error": "Missing API credentials"}

        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "q": query,
                "key": self.api_key,
                "cx": self.search_engine_id,
                "num": num_results,
            }
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                items = response.json().get("items", [])
                results = [
                    {"title": item["title"], "link": item["link"]} for item in items
                ]
                return {"success": True, "result": results}
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
