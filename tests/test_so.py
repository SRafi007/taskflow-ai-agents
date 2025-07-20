# test_basic.py
from models.local_llm import LocalLLM
from agents.system_organizer import create_system_organizer

# Create LLM and agent
llm = LocalLLM()
if llm.is_available():
    agent = create_system_organizer(llm)

    # Test analyzing current directory
    result = agent.analyze_folder(".")
    print("Analysis result:", result)
else:
    print("LLM not available")
