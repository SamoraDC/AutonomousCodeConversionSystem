"""
Language Detection Agent using PydanticAI
Detects programming language from source code with confidence score.
"""

from pydantic_ai import Agent
from ..models.base_models import LanguageDetection
from ..tools.openrouter_client import OpenRouterClient
from typing import Optional


class LanguageDetectionAgent:
    """Agent for detecting programming language from source code."""
    
    def __init__(self, openrouter_client: OpenRouterClient):
        """Initialize the language detection agent.
        
        Args:
            openrouter_client: Configured OpenRouter client
        """
        self.openrouter_client = openrouter_client
        self.system_prompt = self._get_system_prompt()
        self.agent = None  # Will be created lazily
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for language detection."""
        return """You are an expert programming language detection system.

Your task is to analyze source code and determine:
1. The programming language (python, javascript, or typescript)
2. A confidence score from 0.0 to 1.0

Consider these indicators:
- Python: indentation-based syntax, keywords like 'def', 'import', 'class', 'if __name__'
- JavaScript: curly braces, 'function', 'var/let/const', 'console.log'
- TypeScript: like JavaScript but with type annotations, interfaces, 'export type'

Always respond with a valid JSON matching the LanguageDetection schema.
Be conservative with confidence - only give high confidence (>0.8) when very certain."""

    def _get_agent(self) -> Agent:
        """Get or create the PydanticAI agent."""
        if self.agent is None:
            self.agent = Agent(
                model=self.openrouter_client.get_model_name(),
                result_type=LanguageDetection,
                system_prompt=self.system_prompt
            )
        return self.agent

    async def detect_language(self, source_code: str) -> LanguageDetection:
        """Detect programming language from source code.
        
        Args:
            source_code: The source code to analyze
            
        Returns:
            LanguageDetection with language and confidence
        """
        # Use PydanticAI agent to get structured response
        agent = self._get_agent()
        result = await agent.run(
            f"Analyze this source code and detect the programming language:\n\n```\n{source_code}\n```"
        )
        
        return result.data
    
    def detect_language_sync(self, source_code: str) -> LanguageDetection:
        """Synchronous version of language detection.
        
        Args:
            source_code: The source code to analyze
            
        Returns:
            LanguageDetection with language and confidence
        """
        # Use PydanticAI agent to get structured response
        agent = self._get_agent()
        result = agent.run_sync(
            f"Analyze this source code and detect the programming language:\n\n```\n{source_code}\n```"
        )
        
        return result.data


def create_language_detection_agent(openrouter_client: Optional[OpenRouterClient] = None) -> LanguageDetectionAgent:
    """Factory function to create a language detection agent.
    
    Args:
        openrouter_client: Optional pre-configured client, will create default if None
        
    Returns:
        Configured LanguageDetectionAgent
    """
    if openrouter_client is None:
        from ..models.config import load_config
        system_config = load_config()
        openrouter_client = OpenRouterClient(system_config.openrouter)
    
    return LanguageDetectionAgent(openrouter_client) 