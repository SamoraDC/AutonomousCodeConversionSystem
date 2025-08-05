"""
Testes para StateGraph base
"""

import pytest
from unittest.mock import patch

from src.autonomous_code_converter.graphs import create_base_graph, BaseGraphState
from src.autonomous_code_converter.graphs.base_graph import create_initial_state
from src.autonomous_code_converter.models import LanguageType


class TestBaseGraph:
    """Testes para StateGraph base"""
    
    def test_create_initial_state(self):
        """Teste de criação do estado inicial"""
        state = create_initial_state()
        
        assert state.system_state.session_id is not None
        assert len(state.messages) > 0
        assert "Estado inicial criado" in state.messages[0]
        assert state.system_state.current_phase == "initialization"
    
    def test_create_initial_state_with_source(self):
        """Teste de criação do estado com código fonte"""
        source_code = "def hello(): pass"
        language = LanguageType.PYTHON
        
        state = create_initial_state(source_code, language)
        
        assert state.system_state.original_source is not None
        assert state.system_state.original_source.content == source_code
        assert state.system_state.original_source.language == language
    
    def test_base_graph_state_operations(self):
        """Teste das operações do estado do grafo"""
        state = create_initial_state()
        
        # Testar adição de mensagem
        initial_message_count = len(state.messages)
        state.add_message("Teste de mensagem")
        
        assert len(state.messages) == initial_message_count + 1
        assert "Teste de mensagem" in state.messages[-1]
        
        # Testar atualização de fase
        state.update_phase("testing")
        
        assert state.system_state.current_phase == "testing"
        assert "Fase atualizada para: testing" in state.messages[-1]
    
    def test_create_base_graph(self):
        """Teste de criação do grafo base"""
        graph = create_base_graph()
        
        assert graph is not None
        # Verifica se o grafo foi compilado corretamente
        assert hasattr(graph, 'invoke')
        assert hasattr(graph, 'stream')
    
    def test_graph_execution(self):
        """Teste de execução do grafo"""
        graph = create_base_graph()
        initial_state = create_initial_state()
        
        # Executar o grafo
        config = {"configurable": {"thread_id": "test-thread"}}
        result = graph.invoke(initial_state, config=config)
        
        assert result is not None
        assert isinstance(result, dict)
        
        # Converter resultado de volta para BaseGraphState
        result_state = BaseGraphState(**result)
        
        # Verificar se passou pelos nós corretos
        assert result_state.system_state.current_phase == "validated"
        assert len(result_state.messages) >= 3  # inicial + initialization + validation
        
        # Verificar mensagens de log
        messages_text = " ".join(result_state.messages)
        assert "Sistema iniciado" in messages_text
        assert "Validação básica executada" in messages_text


if __name__ == "__main__":
    pytest.main([__file__]) 