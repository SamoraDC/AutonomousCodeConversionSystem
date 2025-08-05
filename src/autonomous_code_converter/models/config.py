"""
Configurações do sistema
"""

import os
from pydantic import BaseModel, Field
from typing import Optional


class OpenRouterConfig(BaseModel):
    """Configuração do OpenRouter"""
    api_key: str = Field(..., description="Chave da API do OpenRouter")
    base_url: str = Field(default="https://openrouter.ai/api/v1", description="URL base da API")
    model: str = Field(default="mistralai/devstral-small:free", description="Modelo a ser usado")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="Temperatura do modelo")
    max_tokens: int = Field(default=4000, gt=0, description="Máximo de tokens")
    timeout: int = Field(default=60, gt=0, description="Timeout em segundos")


class SystemConfig(BaseModel):
    """Configuração geral do sistema"""
    openrouter: OpenRouterConfig
    debug: bool = Field(default=False, description="Modo debug")
    log_level: str = Field(default="INFO", description="Nível de log")
    

def load_config() -> SystemConfig:
    """Carrega configuração a partir das variáveis de ambiente"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY não encontrada nas variáveis de ambiente")
    
    openrouter_config = OpenRouterConfig(api_key=api_key)
    
    return SystemConfig(
        openrouter=openrouter_config,
        debug=os.getenv("DEBUG", "false").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO")
    ) 