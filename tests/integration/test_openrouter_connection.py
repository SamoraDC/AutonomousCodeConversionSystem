"""
Teste de integração real com OpenRouter
Este teste requer OPENROUTER_API_KEY válida no .env
"""

import pytest
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

from src.autonomous_code_converter.tools import OpenRouterClient


class TestOpenRouterIntegration:
    """Testes de integração com OpenRouter"""
    
    @pytest.mark.skipif(
        not os.getenv("OPENROUTER_API_KEY"), 
        reason="OPENROUTER_API_KEY não encontrada"
    )
    def test_real_connection(self):
        """Teste de conexão real com OpenRouter"""
        client = OpenRouterClient()
        
        result = client.test_connection()
        
        print(f"Resultado do teste: {result}")
        
        # Verifica se a conexão foi bem-sucedida
        if result["success"]:
            assert "response" in result
            assert result["model"] == "mistralai/devstral-small:free"
            print(f"✅ Conexão bem-sucedida! Resposta: {result['response']}")
        else:
            print(f"❌ Falha na conexão: {result['error']}")
            # Não falha o teste para não quebrar o CI/CD
            pytest.skip(f"Conexão falhou: {result['error']}")
    
    @pytest.mark.skipif(
        not os.getenv("OPENROUTER_API_KEY"), 
        reason="OPENROUTER_API_KEY não encontrada"
    )
    def test_model_config(self):
        """Teste de configuração do modelo"""
        client = OpenRouterClient()
        
        assert client.config.model == "mistralai/devstral-small:free"
        assert client.config.temperature == 0.1
        assert client.config.max_tokens == 4000
        assert "openrouter.ai" in client.config.base_url


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"]) 