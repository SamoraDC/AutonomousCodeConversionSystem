# Plano do Projeto: Sistema Agêntico Avançado de Conversão de Código para C++

## Visão Geral

Implementação de um sistema agêntico que converte código Python/JavaScript/TypeScript para C++ moderno usando arquitetura LangGraph-Swarm + PydanticAI, com taxa de erro inferior a 1% através de auditoria recursiva.

## Análise do Problema

- **Desafio Principal**: Conversão automática de código entre paradigmas diferentes (dinâmico → estático)
- **Complexidade**: Gerenciamento de memória, tipagem, padrões assíncronos, APIs externas
- **Meta de Qualidade**: <1% de taxa de erro através de auditoria multi-camadas
- **Arquitetura**: Descentralizada (Swarm) vs Hierárquica (Supervisor)

## Lista de Tarefas

### Fase 1: Configuração da Arquitetura Base ✅ CONCLUÍDA

- [x] **1.1** Configurar ambiente de desenvolvimento com uv
- [x] **1.2** Instalar dependências: LangGraph, PydanticAI, OpenRouter SDK
- [x] **1.3** Criar estrutura de diretórios modular do projeto
- [x] **1.4** Definir modelos Pydantic para I/O: SystemState, CodeAnalysisResult, AuditState
- [x] **1.5** Configurar integração OpenRouter com mistralai/devstral-small:free
- [x] **1.6** Implementar StateGraph base com checkpointing

### Fase 2: Agente de Triagem e Abstração Lógica (PydanticAI)

- [x] **2.1** Criar Agent PydanticAI para análise de linguagem (input_type=str, output_type=LanguageDetection)
- [x] **2.2** Implementar Agent para extração de dependências (input_type=SourceCode, output_type=Dependencies)
- [ ] **2.3** Implementar base de conhecimento interna usando informações do api_cpp.md para mapeamento de APIs
- [ ] **2.4** Desenvolver Agent AST com retry mechanisms (input_type=SourceCode, output_type=EnrichedAST)
- [ ] **2.5** Implementar dependency injection para testes com mock APIs
- [ ] **2.6** Criar modelo CodeAnalysisResult como output_type final validado

### Fase 3: Agente de Síntese C++ (PydanticAI)

- [ ] **3.1** Implementar Agent de mapeamento de tipos (input_type=TypeInfo, output_type=CppTypeMapping)
- [ ] **3.2** Criar Agent conversor de memória (input_type=MemoryPattern, output_type=RAIICode)
- [ ] **3.3** Desenvolver Agent de padrões assíncronos (input_type=AsyncPattern, output_type=CoroutineCode)
- [ ] **3.4** Implementar Agent de estruturas de dados (input_type=DataStructure, output_type=STLMapping)
- [ ] **3.5** Criar Agent gerador principal (input_type=CodeAnalysisResult, output_type=CppCodeFiles)
- [ ] **3.6** Integrar streaming responses para geração progressiva de código

### Fase 4: Gerador de Bindings de API

- [ ] **4.1** Implementar recuperador de documentação de APIs (OpenAI, Anthropic, etc.)
- [ ] **4.2** Criar analisador de assinaturas de API (endpoints, headers, schemas)
- [ ] **4.3** Integrar biblioteca HTTP C++ (cpr ou cpp-httplib)
- [ ] **4.4** Implementar gerador de clientes HTTP em C++
- [ ] **4.5** Adicionar suporte para serialização JSON (nlohmann/json)

### Fase 5: Subsistema (SubGraph) de Auditoria Recursiva

- [ ] **5.1** Criar StateGraph para enxame de auditoria
- [ ] **5.2** Implementar modelo AuditState e AuditFinding
- [ ] **5.3** Desenvolver Auditor de Análise Estática (Clang, Cppcheck, Flawfinder)
- [ ] **5.4** Criar Auditor de Modernidade C++ com guia de estilo
- [ ] **5.5** Implementar Auditor de Correção Funcional com GoogleTest
- [ ] **5.6** Criar nó Consolidador para review de descobertas
- [ ] **5.7** Implementar loop recursivo de correção até 0 problemas

### Fase 6: Integração LangGraph + PydanticAI

- [ ] **6.1** Criar StateGraph principal para orquestração dos agentes PydanticAI
- [ ] **6.2** Implementar nós LangGraph que encapsulam agentes PydanticAI
- [ ] **6.3** Configurar arestas condicionais baseadas em output_type dos agentes
- [ ] **6.4** Implementar paralelismo de nós para agentes concorrentes
- [ ] **6.5** Configurar checkpointer com estado Pydantic persistente
- [ ] **6.6** Integrar sistema de routing baseado em validação de schemas

### Fase 7: Configuração do Motor LLM e Integração OpenRouter

- [ ] **7.1** Configurar mistralai/devstral-small:free via OpenRouter como motor principal
- [ ] **7.2** Implementar cliente OpenRouter com autenticação e rate limiting
- [ ] **7.3** Configurar fallbacks para outros modelos gratuitos do OpenRouter
- [ ] **7.4** Otimizar prompts específicos para Devstral (código e análise técnica)
- [ ] **7.5** Implementar sistema de métricas, logging e observabilidade com Logfire

### Fase 8: Testes e Validação com PydanticAI

- [ ] **8.1** Criar suite de testes unitários para cada agente PydanticAI
- [ ] **8.2** Implementar hooks de teste com usuários fictícios (dependency injection)
- [ ] **8.3** Desenvolver testes de integração para fluxo LangGraph completo
- [ ] **8.4** Criar casos de teste para diferentes linguagens de origem (Python/JS/TS)
- [ ] **8.5** Implementar testes de validação de schemas Pydantic I/O
- [ ] **8.6** Criar benchmarks de qualidade e performance
- [ ] **8.7** Validar meta de <1% taxa de erro

### Fase 9: Interface e Documentação

- [ ] **9.1** Criar interface CLI para o sistema
- [ ] **9.2** Implementar interface web opcional (Streamlit/FastAPI)
- [ ] **9.3** Escrever documentação técnica
- [ ] **9.4** Criar exemplos de uso e tutoriais
- [ ] **9.5** Preparar guia de deployment

### Fase 10: Otimização, CI/CD e Deploy

- [ ] **10.1** Otimizar performance do pipeline LangGraph-PydanticAI
- [ ] **10.2** Implementar cache para resultados de análise de código
- [ ] **10.3** Configurar pipeline CI/CD com testes automáticos PydanticAI
- [ ] **10.4** Implementar deploy automatizado com validação de schemas
- [ ] **10.5** Configurar monitoramento em produção com Logfire
- [ ] **10.6** Preparar documentação de manutenção e troubleshooting

## Arquitetura Técnica Resumida

### Stack Principal

- **Orquestração**: LangGraph (StateGraph, nós, arestas, paralelismo, subgraphs)
- **Lógica de Agentes**: PydanticAI (Agent class, input_type/output_type, tool integration)
- **Motor LLM**: mistralai/devstral-small:free via OpenRouter
- **Observabilidade**: Logfire para métricas e logs estruturados
- **Análise Estática**: Clang, Cppcheck, Flawfinder
- **HTTP Client**: cpr library
- **JSON**: nlohmann/json
- **Testes**: GoogleTest + pytest para agentes PydanticAI

### Arquitetura LangGraph-PydanticAI Detalhada

#### **LangGraph - Orquestração Inteligente**

**Função no Sistema:**

- **Sistema Operacional**: Atua como OS para coordenar agentes PydanticAI
- **State Management**: Gerencia estado global compartilhado entre agentes
- **Flow Control**: Controla fluxo de execução com lógica condicional e cíclica
- **Persistence**: Salva e restaura estado para workflows longos

**Capacidades Específicas:**

- Computações cíclicas para feedback loops
- Arestas condicionais baseadas em estado
- Human-in-the-loop para supervisão crítica
- Subgraphs para modularidade (enxame de auditoria)
- Paralelismo de nós para performance
- Checkpointing para recuperação de falhas

#### **PydanticAI - Agentes Especializados Type-Safe**

**Função no Sistema:**

- **Componentes Atômicos**: Cria agentes especializados com responsabilidades bem definidas
- **Validação de I/O**: Garante que entradas e saídas seguem esquemas Pydantic
- **Tool Integration**: Integra ferramentas externas com validação automática
- **Dependency Injection**: Permite injeção de dependências para testes e configuração
- **Multi-Model Support**: Agnóstico a provedores de LLM (OpenRouter)

**Capacidades Específicas:**

- Streaming responses em tempo real
- Retry mechanisms para falhas de validação
- Context management para conversas longas
- Custom tool creation com schemas validados
- Observabilidade nativa via Logfire

### Fluxo de Dados

```
Código Origem → Agente Triagem → Abstração Lógica → 
Agente Síntese → Código C++ → Enxame Auditoria → 
Correções Recursivas → Código Final
```

## Critérios de Sucesso

- [ ] Taxa de erro < 1% em casos de teste
- [ ] Suporte para Python, JavaScript, TypeScript
- [ ] Geração de C++ moderno (C++20)
- [ ] Integração com APIs de LLM
- [ ] Auditoria automática multi-camadas
- [ ] Performance: conversão em <5 minutos para arquivos médios

## Riscos e Mitigações

- **Risco**: Complexidade de mapeamento de tipos → **Mitigação**: Uso extensivo de templates e std::variant
- **Risco**: Dependências C++ complexas → **Mitigação**: CMake automático e gestão de packages
- **Risco**: Qualidade inconsistente → **Mitigação**: Auditoria recursiva multi-agente
- **Risco**: Performance lenta → **Mitigação**: Paralelização e cache

## Padrão de Implementação LangGraph-PydanticAI

### Estrutura de um Agente PydanticAI Típico

```python
from pydantic import BaseModel
from pydanticai import Agent
from typing import Literal

# Schemas de entrada e saída
class SourceCode(BaseModel):
    content: str
    language: Literal["python", "javascript", "typescript"]

class CodeAnalysisResult(BaseModel):
    ast: dict
    dependencies: list[str]
    complexity_score: float

# Definição do agente
analysis_agent = Agent(
    model="mistralai/devstral-small:free",  # OpenRouter
    input_type=SourceCode,
    output_type=CodeAnalysisResult,
    system_prompt="Você é um especialista em análise de código..."
)

# Integração em nó LangGraph
def analysis_node(state: SystemState) -> SystemState:
    result = analysis_agent.run(
        SourceCode(content=state.source_code, language=state.language),
        deps=MockDeps() if testing else RealDeps()  # Dependency injection
    )
    state.analysis_result = result
    return state
```

### Fluxo de Testes com Dependency Injection

```python
# Usuário fictício para testes
class MockDeps:
    def search_web(self, query: str) -> list[str]:
        return ["mock_documentation_url"]

# Teste do agente isoladamente
def test_analysis_agent():
    mock_code = SourceCode(content="def hello(): pass", language="python")
    result = analysis_agent.run(mock_code, deps=MockDeps())
    assert isinstance(result, CodeAnalysisResult)
    assert result.complexity_score > 0
```

## Próximos Passos

1. Revisar e aprovar este plano atualizado
2. Começar pela Fase 1 (Configuração da Arquitetura Base)
3. Implementar agentes PydanticAI com esquemas validados
4. Integrar no StateGraph com paralelismo e checkpointing
5. Teste contínuo com dependency injection

---

*Este plano atualizado integra completamente PydanticAI + LangGraph com mistralai/devstral-small:free via OpenRouter, priorizando type-safety, testabilidade e observabilidade.*
