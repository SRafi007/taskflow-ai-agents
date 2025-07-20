
```
taskflow-ai-agents/
│
├── agents/                           # Agent definitions - Core AI personalities with specific roles
│   ├── __init__.py                   # Package init - Exports agent classes, imports common dependencies
│   ├── planner.py                    # Strategic agent - Breaks down tasks, creates execution plans, coordinates workflow
│   ├── researcher.py                 # Information gatherer - Uses web_search tool, fact-checks, compiles data
│   ├── writer.py                     # Content creator - Takes research data, generates articles/reports/content
│   └── reviewer.py                   # Quality controller - Reviews output, suggests improvements, final approval
│
├── tasks/                            # Task workflows - Orchestrates agents and defines execution flow
│   ├── __init__.py                   # Package init - Exports task classes and workflow utilities
│   └── task_flow.py                  # Main orchestrator - Defines agent sequence, handles data passing, manages state
│
├── tools/                            # External tools - Agent capabilities for interacting with outside world
│   ├── __init__.py                   # Package init - Registers all tools, provides tool discovery mechanism
│   ├── web_search.py                 # Internet search - Takes queries, returns formatted results, handles API calls
│   ├── file_writer.py                # Output generation - Saves content to files, handles various formats (txt, md, docx)
│   ├── file_reader.py                # Input processing - Reads existing files, extracts text, prepares for agents
│   └── reminder_tool.py              # Task scheduling - Sets reminders, tracks deadlines, sends notifications
│
├── models/                           # LLM handling - Model loading and inference management
│   ├── __init__.py                   # Package init - Exports model classes, handles model selection
│   └── local_llm.py                  # Local model interface - Loads local models (Ollama, etc), manages inference
│
├── config/                           # Configuration files - System settings and agent personalities
│   ├── agents_config.yaml            # Agent definitions - Personalities, prompts, tool assignments, behavior rules
│   ├── tasks_config.yaml             # Workflow definitions - Task sequences, dependencies, success criteria
│   └── settings.py                   # System settings - API keys, model paths, logging levels, app configuration
│
├── utils/                            # Utilities - Helper functions and shared functionality
│   ├── __init__.py                   # Package init - Exports utility functions for easy importing
│   ├── topic_formatter.py           # Input processing - Cleans user input, formats topics, validates queries
│   └── logger.py                     # Logging system - Configures logging, handles file/console output, debug info
│
├── ui/                               # User interface - Frontend for user interaction
│   └── app.py                        # Streamlit app - Web interface, user input forms, progress display, results
│
├── output/                           # Generated files - All agent-produced content stored here
│   └── ...                          # Dynamic content - Reports, articles, data files organized by timestamp/task
│
├── tests/                            # Basic tests - Validation and quality assurance
│   ├── test_agents.py                # Agent testing - Unit tests for each agent, mock tool responses, behavior validation
│   ├── test_tools.py                 # Tool testing - API mocking, file I/O tests, error handling validation
│   └── test_tasks.py                 # Workflow testing - End-to-end task execution, integration testing
│
├── examples/                         # Usage examples - Demo scripts and tutorials
│   └── basic_workflow.py             # Getting started - Simple example showing agent coordination, basic task flow
│
├── main.py                           # Entry point - CLI interface, initializes system, handles command-line arguments
├── requirements.txt                  # Dependencies - All Python packages needed, pinned versions for stability
├── .env.example                      # Environment template - Shows required API keys, configuration variables
├── .gitignore                        # Git exclusions - Prevents committing sensitive files, temp files, outputs
└── README.md                         # Documentation - Setup instructions, usage guide, architecture overview
```