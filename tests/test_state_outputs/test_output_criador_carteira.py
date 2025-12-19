"""Testes para o módulo CarteiraWeights."""

import pytest
from pydantic import ValidationError
from portfolio_optimizer.state_otputs.output_criador_carteira import CarteiraWeights


class TestCarteiraWeights:
    """Testes para a classe CarteiraWeights."""

    def test_carteira_weights_valid_creation(self):
        """Testa criação válida de CarteiraWeights."""
        # Arrange
        data = {
            "tickers_weights": {"PETR4.SA": 25.0, "VALE3.SA": 30.0, "ITUB4.SA": 45.0},
            "justification": "Diversificação entre setores de energia, mineração e bancos para reduzir riscos."
        }
        
        # Act
        carteira = CarteiraWeights(**data)
        
        # Assert
        assert carteira.tickers_weights == {"PETR4.SA": 25.0, "VALE3.SA": 30.0, "ITUB4.SA": 45.0}
        assert carteira.justification == "Diversificação entre setores de energia, mineração e bancos para reduzir riscos."

    def test_carteira_weights_empty_tickers(self):
        """Testa CarteiraWeights com tickers vazios."""
        # Arrange
        data = {
            "tickers_weights": {},
            "justification": "Nenhum ativo selecionado devido a condições de mercado desfavoráveis."
        }
        
        # Act
        carteira = CarteiraWeights(**data)
        
        # Assert
        assert carteira.tickers_weights == {}
        assert len(carteira.justification) > 0

    def test_carteira_weights_single_ticker(self):
        """Testa CarteiraWeights com um único ticker."""
        # Arrange
        data = {
            "tickers_weights": {"PETR4.SA": 100.0},
            "justification": "Concentração total em Petrobras devido a oportunidade excepcional."
        }
        
        # Act
        carteira = CarteiraWeights(**data)
        
        # Assert
        assert carteira.tickers_weights == {"PETR4.SA": 100.0}
        assert sum(carteira.tickers_weights.values()) == 100.0

    def test_carteira_weights_justification_max_length(self):
        """Testa validação do tamanho máximo da justificativa."""
        # Arrange
        long_justification = "A" * 1001  # Excede o limite de 1000 caracteres
        data = {
            "tickers_weights": {"PETR4.SA": 100.0},
            "justification": long_justification
        }
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CarteiraWeights(**data)
        
        assert "String should have at most 1000 characters" in str(exc_info.value)

    def test_carteira_weights_justification_exactly_max_length(self):
        """Testa justificativa com exatamente o tamanho máximo."""
        # Arrange
        max_justification = "A" * 1000  # Exatamente 1000 caracteres
        data = {
            "tickers_weights": {"PETR4.SA": 100.0},
            "justification": max_justification
        }
        
        # Act
        carteira = CarteiraWeights(**data)
        
        # Assert
        assert len(carteira.justification) == 1000

    def test_carteira_weights_missing_required_fields(self):
        """Testa erro quando campos obrigatórios estão ausentes."""
        # Test missing tickers_weights
        with pytest.raises(ValidationError) as exc_info:
            CarteiraWeights(justification="Apenas justificativa")
        
        assert "Field required" in str(exc_info.value)
        
        # Test missing justification
        with pytest.raises(ValidationError) as exc_info:
            CarteiraWeights(tickers_weights={"PETR4.SA": 100.0})
        
        assert "Field required" in str(exc_info.value)

    def test_carteira_weights_dict_conversion(self):
        """Testa conversão para dicionário."""
        # Arrange
        data = {
            "tickers_weights": {"PETR4.SA": 60.0, "VALE3.SA": 40.0},
            "justification": "Foco em commodities com maior peso em petróleo."
        }
        carteira = CarteiraWeights(**data)
        
        # Act
        carteira_dict = carteira.model_dump()
        
        # Assert
        assert carteira_dict == data
        assert isinstance(carteira_dict, dict)

    def test_carteira_weights_json_serialization(self):
        """Testa serialização JSON."""
        # Arrange
        data = {
            "tickers_weights": {"PETR4.SA": 70.0, "ITUB4.SA": 30.0},
            "justification": "Combinação de energia e setor financeiro."
        }
        carteira = CarteiraWeights(**data)
        
        # Act
        json_str = carteira.model_dump_json()
        
        # Assert
        assert isinstance(json_str, str)
        assert "PETR4.SA" in json_str
        assert "70.0" in json_str

    def test_carteira_weights_negative_weights(self):
        """Testa pesos negativos (devem ser aceitos pelo modelo)."""
        # Arrange
        data = {
            "tickers_weights": {"PETR4.SA": -10.0, "VALE3.SA": 110.0},
            "justification": "Estratégia de hedge com posição vendida em PETR4."
        }
        
        # Act
        carteira = CarteiraWeights(**data)
        
        # Assert
        assert carteira.tickers_weights["PETR4.SA"] == -10.0
        assert carteira.tickers_weights["VALE3.SA"] == 110.0

    def test_carteira_weights_zero_weights(self):
        """Testa pesos zero."""
        # Arrange
        data = {
            "tickers_weights": {"PETR4.SA": 0.0, "VALE3.SA": 100.0},
            "justification": "Exclusão completa de PETR4 da carteira."
        }
        
        # Act
        carteira = CarteiraWeights(**data)
        
        # Assert
        assert carteira.tickers_weights["PETR4.SA"] == 0.0
        assert carteira.tickers_weights["VALE3.SA"] == 100.0