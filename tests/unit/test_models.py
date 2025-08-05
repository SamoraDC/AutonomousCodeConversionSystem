"""
Testes unitários para os modelos Pydantic
"""

import pytest
from datetime import datetime
from uuid import uuid4

from src.autonomous_code_converter.models import (
    SystemState,
    CodeAnalysisResult,
    AuditState,
    SourceCode,
    LanguageDetection,
    Dependencies,
    EnrichedAST,
    CppCodeFiles,
    AuditFinding,
    LanguageType,
    AuditSeverity
)


class TestSourceCode:
    """Testes para SourceCode"""
    
    def test_source_code_creation(self):
        """Teste de criação básica"""
        source = SourceCode(
            content="def hello(): pass",
            language=LanguageType.PYTHON,
            filename="test.py"
        )
        
        assert source.content == "def hello(): pass"
        assert source.language == LanguageType.PYTHON
        assert source.filename == "test.py"
        assert isinstance(source.metadata, dict)
    
    def test_source_code_validation(self):
        """Teste de validação de campos obrigatórios"""
        with pytest.raises(ValueError):
            SourceCode()  # Campos obrigatórios faltando


class TestLanguageDetection:
    """Testes para LanguageDetection"""
    
    def test_language_detection_creation(self):
        """Teste de criação básica"""
        detection = LanguageDetection(
            detected_language=LanguageType.PYTHON,
            confidence=0.95,
            features_detected=["def", "import", "class"]
        )
        
        assert detection.detected_language == LanguageType.PYTHON
        assert detection.confidence == 0.95
        assert "def" in detection.features_detected
    
    def test_confidence_validation(self):
        """Teste de validação da confiança"""
        with pytest.raises(ValueError):
            LanguageDetection(
                detected_language=LanguageType.PYTHON,
                confidence=1.5  # Deve estar entre 0 e 1
            )


class TestSystemState:
    """Testes para SystemState"""
    
    def test_system_state_creation(self):
        """Teste de criação do estado do sistema"""
        session_id = str(uuid4())
        state = SystemState(session_id=session_id)
        
        assert state.session_id == session_id
        assert state.current_phase == "initialization"
        assert isinstance(state.error_messages, list)
        assert len(state.error_messages) == 0
        assert isinstance(state.created_at, datetime)
        assert isinstance(state.updated_at, datetime)
    
    def test_system_state_with_source(self):
        """Teste com código fonte"""
        source = SourceCode(
            content="console.log('hello');",
            language=LanguageType.JAVASCRIPT
        )
        
        session_id = str(uuid4())
        state = SystemState(
            session_id=session_id,
            original_source=source
        )
        
        assert state.original_source is not None
        assert state.original_source.language == LanguageType.JAVASCRIPT


class TestAuditFinding:
    """Testes para AuditFinding"""
    
    def test_audit_finding_creation(self):
        """Teste de criação de descoberta de auditoria"""
        finding = AuditFinding(
            finding_id="AUDIT-001",
            severity=AuditSeverity.HIGH,
            category="Memory Management",
            description="Potential memory leak detected",
            file_path="main.cpp",
            line_number=42,
            suggested_fix="Use smart pointers instead of raw pointers"
        )
        
        assert finding.finding_id == "AUDIT-001"
        assert finding.severity == AuditSeverity.HIGH
        assert finding.category == "Memory Management"
        assert finding.line_number == 42


class TestCppCodeFiles:
    """Testes para CppCodeFiles"""
    
    def test_cpp_code_files_creation(self):
        """Teste de criação de arquivos C++"""
        cpp_files = CppCodeFiles(
            header_files={"main.hpp": "#pragma once\nclass Main {};"},
            source_files={"main.cpp": "#include \"main.hpp\"\nint main() { return 0; }"},
            cmake_config="cmake_minimum_required(VERSION 3.10)",
            compilation_flags=["-std=c++20", "-O2"]
        )
        
        assert "main.hpp" in cpp_files.header_files
        assert "main.cpp" in cpp_files.source_files
        assert cpp_files.cmake_config.startswith("cmake_minimum_required")
        assert "-std=c++20" in cpp_files.compilation_flags


if __name__ == "__main__":
    pytest.main([__file__]) 