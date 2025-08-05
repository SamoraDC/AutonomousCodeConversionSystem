"""
StateGraph base para o sistema de conversão de código
"""

from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, Field

from ..models.base_models import SystemState, SourceCode, LanguageType


class BaseGraphState(BaseModel):
    """Estado base para os grafos LangGraph"""
    system_state: SystemState = Field(..., description="Estado do sistema")
    messages: list[str] = Field(default_factory=list, description="Mensagens de log")
    
    def add_message(self, message: str):
        """Adiciona uma mensagem de log"""
        timestamp = datetime.now().isoformat()
        self.messages.append(f"[{timestamp}] {message}")
    
    def update_phase(self, phase: str):
        """Atualiza a fase atual"""
        self.system_state.current_phase = phase
        self.system_state.updated_at = datetime.now()
        self.add_message(f"Fase atualizada para: {phase}")


def initialization_node(state: BaseGraphState) -> BaseGraphState:
    """Nó de inicialização do sistema"""
    state.add_message("Sistema iniciado")
    state.update_phase("initialized")
    
    return state


def validation_node(state: BaseGraphState) -> BaseGraphState:
    """Nó de validação básica"""
    state.add_message("Validação básica executada")
    
    # Validação básica do estado
    if not state.system_state.session_id:
        state.system_state.error_messages.append("Session ID não encontrado")
    
    state.update_phase("validated")
    return state


def create_base_graph() -> StateGraph:
    """
    Cria o grafo base do sistema com checkpointing
    """
    # Configurar o checkpointer em memória
    checkpointer = MemorySaver()
    
    # Criar o grafo
    workflow = StateGraph(BaseGraphState)
    
    # Adicionar nós
    workflow.add_node("initialization", initialization_node)
    workflow.add_node("validation", validation_node)
    
    # Definir fluxo
    workflow.add_edge(START, "initialization")
    workflow.add_edge("initialization", "validation")
    workflow.add_edge("validation", END)
    
    # Compilar com checkpointing
    graph = workflow.compile(checkpointer=checkpointer)
    
    return graph


def create_initial_state(source_code: Optional[str] = None, 
                        language: Optional[LanguageType] = None) -> BaseGraphState:
    """
    Cria o estado inicial do sistema
    """
    session_id = str(uuid.uuid4())
    
    # Criar SystemState
    system_state = SystemState(session_id=session_id)
    
    # Se código fonte foi fornecido, adicionar ao estado
    if source_code and language:
        system_state.original_source = SourceCode(
            content=source_code,
            language=language
        )
    
    # Criar estado do grafo
    graph_state = BaseGraphState(system_state=system_state)
    graph_state.add_message("Estado inicial criado")
    
    return graph_state 