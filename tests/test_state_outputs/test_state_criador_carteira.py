"""Testes para o módulo StateCarteira."""

import pytest
from portfolio_optimizer.state_otputs.state_criador_carteira import StateCarteira


class TestStateCarteira:
    """Testes para a classe StateCarteira."""

    def test_state_carteira_creation(self):
        """Testa a criação de um StateCarteira válido."""
        # Arrange
        state_data = {
            "tickers_weights": {"PETR4.SA": 25.0, "VALE3.SA": 30.0, "ITUB4.SA": 45.0},
            "justification": "Diversificação entre setores",
            "analise_avaliador_weights": "Pesos bem distribuídos",
            "avaliacao_acoes": "Análise técnica favorável",
            "correlacao_acoes": "Baixa correlação entre ativos",
            "interacao": 1,
            "soma_weights_error": "",
            "tics": ["PETR4.SA", "VALE3.SA", "ITUB4.SA"],
            "tics_error": ""
        }
        
        # Act
        state = StateCarteira(state_data)
        
        # Assert
        assert state["tickers_weights"] == {"PETR4.SA": 25.0, "VALE3.SA": 30.0, "ITUB4.SA": 45.0}
        assert state["justification"] == "Diversificação entre setores"
        assert state["interacao"] == 1
        assert state["tics"] == ["PETR4.SA", "VALE3.SA", "ITUB4.SA"]

    def test_state_carteira_empty_weights(self):
        """Testa StateCarteira com pesos vazios."""
        # Arrange
        state_data = {
            "tickers_weights": {},
            "justification": "",
            "analise_avaliador_weights": "",
            "avaliacao_acoes": "",
            "correlacao_acoes": "",
            "interacao": 0,
            "soma_weights_error": "Erro na soma dos pesos",
            "tics": [],
            "tics_error": "Nenhum ticker válido"
        }
        
        # Act
        state = StateCarteira(state_data)
        
        # Assert
        assert state["tickers_weights"] == {}
        assert state["soma_weights_error"] == "Erro na soma dos pesos"
        assert state["tics_error"] == "Nenhum ticker válido"

    def test_state_carteira_access_keys(self):
        """Testa acesso às chaves do StateCarteira."""
        # Arrange
        state_data = {
            "tickers_weights": {"PETR4.SA": 50.0, "VALE3.SA": 50.0},
            "justification": "Estratégia conservadora",
            "analise_avaliador_weights": "Análise positiva",
            "avaliacao_acoes": "Ações bem avaliadas",
            "correlacao_acoes": "Correlação moderada",
            "interacao": 2,
            "soma_weights_error": "",
            "tics": ["PETR4.SA", "VALE3.SA"],
            "tics_error": ""
        }
        
        # Act
        state = StateCarteira(state_data)
        
        # Assert
        assert "tickers_weights" in state
        assert "justification" in state
        assert "analise_avaliador_weights" in state
        assert "avaliacao_acoes" in state
        assert "correlacao_acoes" in state
        assert "interacao" in state
        assert "soma_weights_error" in state
        assert "tics" in state
        assert "tics_error" in state

    def test_state_carteira_update_values(self):
        """Testa atualização de valores no StateCarteira."""
        # Arrange
        state_data = {
            "tickers_weights": {"PETR4.SA": 100.0},
            "justification": "Concentração inicial",
            "analise_avaliador_weights": "",
            "avaliacao_acoes": "",
            "correlacao_acoes": "",
            "interacao": 1,
            "soma_weights_error": "",
            "tics": ["PETR4.SA"],
            "tics_error": ""
        }
        
        # Act
        state = StateCarteira(state_data)
        state["tickers_weights"] = {"PETR4.SA": 50.0, "VALE3.SA": 50.0}
        state["justification"] = "Diversificação aplicada"
        state["interacao"] = 2
        
        # Assert
        assert state["tickers_weights"] == {"PETR4.SA": 50.0, "VALE3.SA": 50.0}
        assert state["justification"] == "Diversificação aplicada"
        assert state["interacao"] == 2