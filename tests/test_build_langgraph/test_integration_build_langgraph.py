"""Testes de integração para o módulo build_langgraph."""

import pytest
from unittest.mock import Mock, patch


class TestBuildLangGraphIntegration:
    """Testes de integração para o módulo build_langgraph."""

    def test_module_imports(self):
        """Testa se o módulo pode ser importado corretamente."""
        try:
            from portfolio_optimizer.build_langgraph import BuildGraphCriadorCarteira, BuildGraphAvaliacaoTics
            
            assert BuildGraphCriadorCarteira is not None
            assert BuildGraphAvaliacaoTics is not None
            
            builder1 = BuildGraphCriadorCarteira()
            builder2 = BuildGraphAvaliacaoTics()
            
            assert builder1 is not None
            assert builder2 is not None
            
        except ImportError:
            pytest.skip("Módulo não disponível devido a dependências")

    def test_both_builders_can_coexist(self):
        """Testa se ambos os builders podem coexistir."""
        try:
            from portfolio_optimizer.build_langgraph.graph_criador_carteira import BuildGraphCriadorCarteira
            from portfolio_optimizer.build_langgraph.graph_avaliacao_tics import BuildGraphAvaliacaoTics
            
            builder1 = BuildGraphCriadorCarteira()
            builder2 = BuildGraphAvaliacaoTics()
            
            assert builder1 is not builder2
            assert builder1.graph is not builder2.graph
            assert type(builder1) != type(builder2)
            
        except ImportError:
            pytest.skip("Módulo não disponível devido a dependências")

    def test_node_function_workflow_integration(self):
        """Testa integração das funções dos nós."""
        try:
            from portfolio_optimizer.build_langgraph.nodes_criador_carteira import should_continue
            
            scenarios = [
                {"interacao": 1, "tics_error": None, "expected": "analista_avaliador_peso_carteira"},
                {"interacao": 3, "tics_error": None, "expected": "END"},
                {"interacao": 1, "tics_error": "error", "expected": "analista_avaliador_peso_carteira"},
            ]
            
            for scenario in scenarios:
                state = {
                    "interacao": scenario["interacao"],
                    "tics_error": scenario["tics_error"]
                }
                result = should_continue(state)
                assert result == scenario["expected"]
                
        except ImportError:
            pytest.skip("Módulo não disponível devido a dependências")

    def test_verifica_tics_workflow_integration(self):
        """Testa integração da verificação de tickers."""
        try:
            from portfolio_optimizer.build_langgraph.nodes_criador_carteira import verifica_tics_selecionados
            
            test_cases = [
                {
                    "state": {
                        "tickers_weights": {"PETR4.SA": 50.0, "VALE3.SA": 50.0},
                        "tics": ["PETR4.SA", "VALE3.SA", "ITUB4.SA"]
                    },
                    "should_have_error": False
                },
                {
                    "state": {
                        "tickers_weights": {"PETR4.SA": 50.0, "INVALID.SA": 50.0},
                        "tics": ["PETR4.SA", "VALE3.SA", "ITUB4.SA"]
                    },
                    "should_have_error": True
                }
            ]
            
            for i, test_case in enumerate(test_cases):
                result = verifica_tics_selecionados(test_case["state"])
                
                assert isinstance(result, dict)
                assert "tics_error" in result
                
                if test_case["should_have_error"]:
                    assert result["tics_error"] is not None
                else:
                    assert result["tics_error"] is None
                    
        except ImportError:
            pytest.skip("Módulo não disponível devido a dependências")