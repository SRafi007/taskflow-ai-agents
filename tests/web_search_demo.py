# examples/web_search_demo.py

from agents.web_intelligence import WebIntelligenceAgent
from tools.web_search import WebSearchTool
from tools.base_tool import register_tool

# Register tool
register_tool(WebSearchTool())

# Initialize and run agent
agent = WebIntelligenceAgent()
result = agent.execute_task("What are the latest updates on AI in healthcare?")
print(result)
