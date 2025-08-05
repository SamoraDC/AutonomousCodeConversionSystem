"""
Dependency Extraction Agent using PydanticAI
Extracts imports, libraries, and documentation URLs from source code.
"""

from pydantic_ai import Agent
from ..models.base_models import SourceCode, Dependencies
from ..tools.openrouter_client import OpenRouterClient
from typing import Optional


class DependencyExtractionAgent:
    """Agent for extracting dependencies from source code."""
    
    def __init__(self, openrouter_client: OpenRouterClient):
        """Initialize the dependency extraction agent.
        
        Args:
            openrouter_client: Configured OpenRouter client
        """
        self.openrouter_client = openrouter_client
        self.system_prompt = self._get_system_prompt()
        self.agent = None  # Will be created lazily
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for dependency extraction."""
        return """You are an expert dependency extraction system for code analysis.

Your task is to analyze source code and extract:
1. imports: All import/include statements found in the code
2. external_libraries: Third-party libraries/packages being used
3. standard_libraries: Built-in/standard library modules being used
4. documentation_urls: Relevant documentation URLs for the libraries

Language-specific patterns:
- Python: 'import', 'from...import', pip packages, standard library (os, sys, json, etc.)
- JavaScript: 'import', 'require()', npm packages, built-ins (fs, path, http, etc.)
- TypeScript: Same as JavaScript + type imports, @types packages

For documentation_urls, provide official documentation links when possible:
- Python: https://docs.python.org/ or PyPI pages
- JavaScript/Node.js: https://nodejs.org/docs/ or npm registry
- TypeScript: https://www.typescriptlang.org/docs/

Always respond with a valid JSON matching the Dependencies schema.
Be thorough but accurate - only include dependencies that are actually present."""

    def _get_agent(self) -> Agent:
        """Get or create the PydanticAI agent."""
        if self.agent is None:
            self.agent = Agent(
                model=self.openrouter_client.get_model_name(),
                result_type=Dependencies,
                system_prompt=self.system_prompt
            )
        return self.agent

    async def extract_dependencies(self, source_code: SourceCode) -> Dependencies:
        """Extract dependencies from source code.
        
        Args:
            source_code: The source code to analyze
            
        Returns:
            Dependencies with imports, libraries, and documentation
        """
        # Use PydanticAI agent to get structured response
        agent = self._get_agent()
        
        # Prepare context for the agent
        context = f"""
Language: {source_code.language.value}
Filename: {source_code.filename or 'unknown'}

Source Code:
```{source_code.language.value}
{source_code.content}
```

Analyze this code and extract all dependencies.
"""
        
        result = await agent.run(context)
        return result.data
    
    def extract_dependencies_sync(self, source_code: SourceCode) -> Dependencies:
        """Synchronous version of dependency extraction.
        
        Args:
            source_code: The source code to analyze
            
        Returns:
            Dependencies with imports, libraries, and documentation
        """
        # Use PydanticAI agent to get structured response
        agent = self._get_agent()
        
        # Prepare context for the agent
        context = f"""
Language: {source_code.language.value}
Filename: {source_code.filename or 'unknown'}

Source Code:
```{source_code.language.value}
{source_code.content}
```

Analyze this code and extract all dependencies.
"""
        
        result = agent.run_sync(context)
        return result.data


def create_dependency_extraction_agent(openrouter_client: Optional[OpenRouterClient] = None) -> DependencyExtractionAgent:
    """Factory function to create a dependency extraction agent.
    
    Args:
        openrouter_client: Optional pre-configured client, will create default if None
        
    Returns:
        Configured DependencyExtractionAgent
    """
    if openrouter_client is None:
        from ..models.config import load_config
        system_config = load_config()
        openrouter_client = OpenRouterClient(system_config.openrouter)
    
    return DependencyExtractionAgent(openrouter_client) 