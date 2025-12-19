"""Testes para o módulo de funções utilitárias."""

import pytest
import json
import pandas as pd
from unittest.mock import Mock, patch
from portfolio_optimizer.utils.funcoes_utilitarias import (
    tratando_resposta_router_llm,
    normalizar_pesos,
    transformando_data_frame_para_markdown
)


class TestTratandoRespostaRouterLlm:
    """Testes para a função tratando_resposta_router_llm."""

    def test_response_with_output_attribute(self):
        """Testa resposta com atributo output."""
        mock_response = Mock()
        mock_output = {"field1": "value1", "field2": "value2"}
        mock_response.output = mock_output
        
        result = tratando_resposta_router_llm(mock_response)
        
        assert result == {"field1": "value1", "field2": "value2"}

    def test_response_with_dict_method_and_model_class(self):
        """Testa resposta com método dict e model_class."""
        # Simular um objeto Pydantic com método dict
        class MockPydanticResponse:
            def dict(self):
                return {"field1": "value1", "field2": "value2"}
        
        mock_response = MockPydanticResponse()
        mock_model_class = Mock()
        mock_model_class.__fields__ = {"field1": None, "field2": None}
        
        result = tratando_resposta_router_llm(mock_response, mock_model_class)
        
        assert result == {"field1": "value1", "field2": "value2"}

    def test_response_is_dict(self):
        """Testa resposta que já é um dicionário."""
        response = {"field1": "value1", "field2": "value2"}
        
        result = tratando_resposta_router_llm(response)
        
        assert result == {"field1": "value1", "field2": "value2"}

    def test_response_is_valid_json_string(self):
        """Testa resposta que é uma string JSON válida."""
        response = '{"field1": "value1", "field2": "value2"}'
        
        result = tratando_resposta_router_llm(response)
        
        assert result == {"field1": "value1", "field2": "value2"}

    def test_response_is_invalid_json_string(self):
        """Testa resposta que é uma string JSON inválida."""
        response = 'invalid json string'
        
        result = tratando_resposta_router_llm(response)
        
        assert result == {}


class TestNormalizarPesos:
    """Testes para a função normalizar_pesos."""

    def test_pesos_ja_normalizados(self):
        """Testa pesos que já estão normalizados."""
        weights = {"PETR4.SA": 25.0, "VALE3.SA": 25.0, "ITUB4.SA": 25.0, "BBDC4.SA": 25.0}
        
        result = normalizar_pesos(weights)
        
        assert result == weights
        assert sum(result.values()) == 100.0

    def test_normalizacao_proporcional(self):
        """Testa normalização proporcional."""
        weights = {"PETR4.SA": 20.0, "VALE3.SA": 30.0, "ITUB4.SA": 25.0, "BBDC4.SA": 15.0}
        
        result = normalizar_pesos(weights)
        
        assert abs(sum(result.values()) - 100.0) < 0.001
        assert abs(result["PETR4.SA"] - 22.222) < 0.01
        assert abs(result["VALE3.SA"] - 33.333) < 0.01

    def test_pesos_vazios(self):
        """Testa com dicionário vazio."""
        weights = {}
        
        with pytest.raises(ZeroDivisionError):
            normalizar_pesos(weights)


class TestTransformandoDataFrameParaMarkdown:
    """Testes para a função transformando_data_frame_para_markdown."""

    def test_transformacao_sucesso(self):
        """Testa transformação bem-sucedida."""
        results = {
            "PETR4.SA": {"classification": "BUY", "analysis": "Strong fundamentals"},
            "VALE3.SA": {"classification": "HOLD", "analysis": "Moderate outlook"}
        }
        
        result = transformando_data_frame_para_markdown(results)
        
        assert isinstance(result, str)
        assert "PETR4.SA" in result
        assert "VALE3.SA" in result
        assert "BUY" in result
        assert "HOLD" in result