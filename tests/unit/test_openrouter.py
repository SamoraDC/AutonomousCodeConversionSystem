"""
Testes para integração OpenRouter
"""

import pytest
import os
from unittest.mock import patch, MagicMock

from src.autonomous_code_converter.tools import OpenRouterClient
from src.autonomous_code_converter.models.config import OpenRouterConfig


class TestOpenRouterClient:
    """Testes para OpenRouterClient"""
    
    def test_config_validation(self):
        """Teste de validação de configuração"""
        config = OpenRouterConfig(api_key="test-key")
        
        assert config.api_key == "test-key"
        assert config.model == "mistralai/devstral-small:free"
        assert config.base_url == "https://openrouter.ai/api/v1"
        assert config.temperature == 0.1
        assert config.max_tokens == 4000
    
    def test_openrouter_client_creation(self):
        """Teste de criação do cliente"""
        config = OpenRouterConfig(api_key="test-key")
        client = OpenRouterClient(config)
        
        assert client.config.api_key == "test-key"
        assert client.client is not None
        assert client.model_name == "mistralai/devstral-small:free"
    
    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-env-key"})
    def test_config_from_env(self):
        """Teste de carregamento de configuração do ambiente"""
        from src.autonomous_code_converter.models.config import load_config
        
        config = load_config()
        assert config.openrouter.api_key == "test-env-key"
    
    def test_missing_api_key(self):
        """Teste de erro quando API key está faltando"""
        with patch.dict(os.environ, {}, clear=True):
            from src.autonomous_code_converter.models.config import load_config
            
            with pytest.raises(ValueError, match="OPENROUTER_API_KEY não encontrada"):
                load_config()
    
    def test_agent_creation_method_exists(self):
        """Teste de existência do método de criação de agente"""
        config = OpenRouterConfig(api_key="test-key")
        client = OpenRouterClient(config)
        
        # Verifica se o método existe
        assert hasattr(client, 'create_agent')
        assert callable(client.create_agent)
        
        # Verifica se o modelo está configurado corretamente
        assert client.model_name == "mistralai/devstral-small:free"


if __name__ == "__main__":
    pytest.main([__file__]) 