"""
Modelos base Pydantic para o sistema de conversão de código
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional, Literal, Union
from datetime import datetime
from enum import Enum


class LanguageType(str, Enum):
    """Tipos de linguagem suportados"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"


class AuditSeverity(str, Enum):
    """Níveis de severidade para auditoria"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SourceCode(BaseModel):
    """Código fonte de entrada"""
    content: str = Field(..., description="Conteúdo do código fonte")
    language: LanguageType = Field(..., description="Linguagem do código")
    filename: Optional[str] = Field(None, description="Nome do arquivo")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadados adicionais")


class LanguageDetection(BaseModel):
    """Resultado da detecção de linguagem"""
    detected_language: LanguageType = Field(..., description="Linguagem detectada")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confiança na detecção")
    features_detected: List[str] = Field(default_factory=list, description="Características detectadas")


class Dependencies(BaseModel):
    """Dependências do código"""
    imports: List[str] = Field(default_factory=list, description="Imports/includes encontrados")
    external_libraries: List[str] = Field(default_factory=list, description="Bibliotecas externas")
    standard_libraries: List[str] = Field(default_factory=list, description="Bibliotecas padrão")
    documentation_urls: Dict[str, str] = Field(default_factory=dict, description="URLs de documentação")


class EnrichedAST(BaseModel):
    """AST enriquecida com descrições"""
    ast_nodes: Dict[str, Any] = Field(..., description="Nós da AST")
    function_descriptions: Dict[str, str] = Field(default_factory=dict, description="Descrições de funções")
    variable_roles: Dict[str, str] = Field(default_factory=dict, description="Papéis das variáveis")
    control_flow_logic: List[str] = Field(default_factory=list, description="Lógica de fluxo de controle")
    complexity_metrics: Dict[str, Union[int, float]] = Field(default_factory=dict, description="Métricas de complexidade")


class CodeAnalysisResult(BaseModel):
    """Resultado da análise de código"""
    source_code: SourceCode = Field(..., description="Código fonte original")
    language_detection: LanguageDetection = Field(..., description="Detecção de linguagem")
    dependencies: Dependencies = Field(..., description="Dependências identificadas")
    enriched_ast: EnrichedAST = Field(..., description="AST enriquecida")
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da análise")


class CppCodeFiles(BaseModel):
    """Arquivos de código C++ gerados"""
    header_files: Dict[str, str] = Field(default_factory=dict, description="Arquivos .hpp")
    source_files: Dict[str, str] = Field(default_factory=dict, description="Arquivos .cpp")
    cmake_config: Optional[str] = Field(None, description="Configuração CMake")
    compilation_flags: List[str] = Field(default_factory=list, description="Flags de compilação")
    dependencies_info: Dict[str, str] = Field(default_factory=dict, description="Informações de dependências")


class AuditFinding(BaseModel):
    """Descoberta de auditoria"""
    finding_id: str = Field(..., description="ID único da descoberta")
    severity: AuditSeverity = Field(..., description="Severidade da descoberta")
    category: str = Field(..., description="Categoria da descoberta")
    description: str = Field(..., description="Descrição da descoberta")
    file_path: Optional[str] = Field(None, description="Caminho do arquivo")
    line_number: Optional[int] = Field(None, description="Número da linha")
    suggested_fix: Optional[str] = Field(None, description="Correção sugerida")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadados adicionais")


class AuditState(BaseModel):
    """Estado da auditoria"""
    code_files: CppCodeFiles = Field(..., description="Arquivos de código")
    findings: List[AuditFinding] = Field(default_factory=list, description="Descobertas de auditoria")
    iteration_count: int = Field(default=0, description="Contador de iterações")
    is_complete: bool = Field(default=False, description="Auditoria completa")
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Pontuação de qualidade")


class SystemState(BaseModel):
    """Estado global do sistema"""
    # Dados de entrada
    original_source: Optional[SourceCode] = Field(None, description="Código fonte original")
    
    # Resultados de análise
    analysis_result: Optional[CodeAnalysisResult] = Field(None, description="Resultado da análise")
    
    # Código C++ gerado
    cpp_code: Optional[CppCodeFiles] = Field(None, description="Código C++ gerado")
    
    # Estado da auditoria
    audit_state: Optional[AuditState] = Field(None, description="Estado da auditoria")
    
    # Controle de fluxo
    current_phase: str = Field(default="initialization", description="Fase atual")
    error_messages: List[str] = Field(default_factory=list, description="Mensagens de erro")
    
    # Metadados
    session_id: str = Field(..., description="ID da sessão")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp de criação")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp de atualização")
    
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    ) 