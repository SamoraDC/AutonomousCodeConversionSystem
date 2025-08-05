"""
Cliente OpenRouter para PydanticAI
"""

import os
from typing import Any, Dict
from openai import OpenAI
from pydantic_ai import Agent

from ..models.config import OpenRouterConfig, load_config


class OpenRouterClient:
    """Cliente para OpenRouter integrado com PydanticAI"""
    
    def __init__(self, config: OpenRouterConfig = None):
        """Inicializa o cliente OpenRouter"""
        if config is None:
            system_config = load_config()
            config = system_config.openrouter
        
        self.config = config
        
        # Cliente OpenAI compatível com OpenRouter
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
        
        # Configuração do modelo para PydanticAI
        self.model_name = config.model
    
    def get_model_name(self) -> str:
        """Retorna o nome do modelo configurado"""
        return f"openai:{self.model_name}"
    
    def create_agent(self, system_prompt: str, **kwargs) -> Agent:
        """Cria um agente PydanticAI com configurações do OpenRouter"""
        # Usando diretamente o modelo OpenAI com configuração customizada
        return Agent(
            model=self.get_model_name(),
            system_prompt=system_prompt,
            **kwargs
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """Testa a conexão com OpenRouter"""
        try:
            # Teste simples de conexão
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            
            return {
                "success": True,
                "model": self.config.model,
                "response": response.choices[0].message.content,
                "usage": response.usage.model_dump() if response.usage else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 