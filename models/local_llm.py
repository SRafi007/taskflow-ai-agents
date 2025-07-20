# models/local_llm.py
"""
Local LLM interface using Ollama
Handles loading and running Mistral model locally
"""

import requests
import json
from typing import Dict, Any, Optional


class LocalLLM:
    """
    Simple interface to interact with Ollama running Mistral
    """

    def __init__(
        self, model_name: str = "mistral", base_url: str = "http://localhost:11434"
    ):
        """
        Initialize the local LLM

        Args:
            model_name: Name of the model in Ollama (default: mistral)
            base_url: Ollama API URL (default: http://localhost:11434)
        """
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"

        print(f"Initialized LocalLLM with model: {model_name}")

    def generate(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """
        Generate text using the local model

        Args:
            prompt: The input prompt for the model
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0 = focused, 1.0 = creative)

        Returns:
            Generated text response
        """
        try:
            # Prepare the request data for Ollama
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,  # Get complete response at once
                "options": {"num_predict": max_tokens, "temperature": temperature},
            }

            # Make the request to Ollama
            print(f"Sending request to Ollama...")
            response = requests.post(
                self.api_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=120,  # 2 minute timeout
            )

            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "")
                print(f"Generated {len(generated_text)} characters")
                return generated_text
            else:
                error_msg = (
                    f"Error from Ollama: {response.status_code} - {response.text}"
                )
                print(error_msg)
                return f"Error: {error_msg}"

        except requests.exceptions.ConnectionError:
            error_msg = "Cannot connect to Ollama. Make sure Ollama is running on localhost:11434"
            print(error_msg)
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(error_msg)
            return f"Error: {error_msg}"

    def is_available(self) -> bool:
        """
        Check if Ollama is running and the model is available

        Returns:
            True if model is ready, False otherwise
        """
        try:
            # Check if Ollama is running
            health_url = f"{self.base_url}/api/tags"
            response = requests.get(health_url, timeout=5)

            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]

                if any(self.model_name in name for name in model_names):
                    print(f"✅ Model '{self.model_name}' is available")
                    return True
                else:
                    print(
                        f"❌ Model '{self.model_name}' not found. Available models: {model_names}"
                    )
                    return False
            else:
                print(f"❌ Ollama not responding properly: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Cannot reach Ollama: {e}")
            return False

    def chat(
        self, messages: list, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """
        Chat-style interaction (converts messages to single prompt)

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Creativity level

        Returns:
            Generated response
        """
        # Convert chat messages to a single prompt
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        # Add final prompt for assistant response
        prompt_parts.append("Assistant:")
        full_prompt = "\n\n".join(prompt_parts)

        return self.generate(full_prompt, max_tokens, temperature)


# Example usage:
if __name__ == "__main__":
    # Test the model
    llm = LocalLLM()

    if llm.is_available():
        response = llm.generate("Hello! How are you today?")
        print(f"Model response: {response}")
    else:
        print("Model is not available. Make sure Ollama is running with Mistral model.")
