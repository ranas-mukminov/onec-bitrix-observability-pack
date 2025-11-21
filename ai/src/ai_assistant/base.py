from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Generate a completion for the given prompt."""
        pass

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Chat with the AI model."""
        pass

class NoopAIProvider(AIProvider):
    """No-op provider for offline/testing mode."""

    def complete(self, prompt: str) -> str:
        return "AI Analysis is disabled or running in offline mode."

    def chat(self, messages: List[Dict[str, str]]) -> str:
        return "AI Analysis is disabled or running in offline mode."
