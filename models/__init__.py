# models/__init__.py
"""
Model package initialization
Exports the main model classes for easy importing
"""

from .local_llm import LocalLLM

# Make it easy to import the main model class
__all__ = ["LocalLLM"]

# You can import like: from models import LocalLLM
