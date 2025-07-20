# config/settings.py
"""
System settings and configuration
Loads environment variables and sets up app-wide settings
"""

import os
from pathlib import Path
from typing import Dict, Any

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


class Settings:
    """
    Centralized settings management
    Loads from environment variables with sensible defaults
    """

    def __init__(self):
        """Load all settings from environment variables"""

        # === MODEL SETTINGS ===
        self.MODEL_NAME = os.getenv("MODEL_NAME", "mistral")
        self.OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "1000"))
        self.DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))

        # === API SETTINGS ===
        # Add these to your .env file if you want to use external APIs
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")  # For search
        self.GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")

        # === FILE PATHS ===
        self.OUTPUT_DIR = PROJECT_ROOT / "output"
        self.LOGS_DIR = PROJECT_ROOT / "logs"
        self.CONFIG_DIR = PROJECT_ROOT / "config"

        # === LOGGING SETTINGS ===
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_TO_FILE = os.getenv("LOG_TO_FILE", "true").lower() == "true"
        self.LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", "taskflow.log")

        # === UI SETTINGS ===
        self.STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
        self.APP_TITLE = os.getenv("APP_TITLE", "TaskFlow AI Agents")

        # === AGENT SETTINGS ===
        self.MAX_AGENT_RETRIES = int(os.getenv("MAX_AGENT_RETRIES", "3"))
        self.AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "300"))  # 5 minutes

        # === TOOL SETTINGS ===
        self.SEARCH_RESULTS_LIMIT = int(os.getenv("SEARCH_RESULTS_LIMIT", "5"))
        self.FILE_SIZE_LIMIT_MB = int(os.getenv("FILE_SIZE_LIMIT_MB", "10"))

        # Create necessary directories
        self._create_directories()

    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [self.OUTPUT_DIR, self.LOGS_DIR]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"📁 Directory ready: {directory}")

    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration for easy passing to LLM"""
        return {
            "model_name": self.MODEL_NAME,
            "base_url": self.OLLAMA_BASE_URL,
            "max_tokens": self.DEFAULT_MAX_TOKENS,
            "temperature": self.DEFAULT_TEMPERATURE,
        }

    def get_file_paths(self) -> Dict[str, Path]:
        """Get all important file paths"""
        return {
            "output_dir": self.OUTPUT_DIR,
            "logs_dir": self.LOGS_DIR,
            "config_dir": self.CONFIG_DIR,
            "agents_config": self.CONFIG_DIR / "agents_config.yaml",
            "tasks_config": self.CONFIG_DIR / "tasks_config.yaml",
        }

    def is_development_mode(self) -> bool:
        """Check if running in development mode"""
        return os.getenv("ENV", "development") == "development"

    def print_config(self):
        """Print current configuration for debugging"""
        print("\n" + "=" * 50)
        print("🔧 TASKFLOW AI AGENTS CONFIGURATION")
        print("=" * 50)
        print(f"Model: {self.MODEL_NAME}")
        print(f"Ollama URL: {self.OLLAMA_BASE_URL}")
        print(f"Max Tokens: {self.DEFAULT_MAX_TOKENS}")
        print(f"Temperature: {self.DEFAULT_TEMPERATURE}")
        print(f"Output Directory: {self.OUTPUT_DIR}")
        print(f"Log Level: {self.LOG_LEVEL}")
        print(f"Development Mode: {self.is_development_mode()}")
        print("=" * 50 + "\n")


# Create a global settings instance
settings = Settings()


# Convenience functions for easy importing
def get_settings() -> Settings:
    """Get the global settings instance"""
    return settings


def get_model_config() -> Dict[str, Any]:
    """Quick access to model configuration"""
    return settings.get_model_config()


def get_file_paths() -> Dict[str, Path]:
    """Quick access to file paths"""
    return settings.get_file_paths()


# Example usage and testing
if __name__ == "__main__":
    # Test the settings
    settings.print_config()

    # Test directory creation
    print("File paths:", get_file_paths())
    print("Model config:", get_model_config())
