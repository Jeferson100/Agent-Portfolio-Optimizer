"""Testes para o módulo VerificadorTicks."""

import pytest
from unittest.mock import patch, Mock
import pandas as pd
from portfolio_optimizer.coleta_dados.verificador_ticks import VerificadorTicks


class TestVerificadorTicks:
    """Testes para a classe VerificadorTicks."""

    def test_init(self):
        """Testa a inicialização da classe."""
        verificador = VerificadorTicks("PETR4.SA")
        assert verificador.tic == "PETR4.SA"

    @patch('pandas.read_csv')
    def test_obtendo_ticks_success(self, mock_read_csv):
        """Testa a obtenção de tickers com sucesso."""
        # Arrange
        mock_df = pd.DataFrame({'tic': ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA']})
        mock_read_csv.return_value = mock_df
        verificador = VerificadorTicks("PETR4.SA")
        
        # Act
        result = verificador.obtendo_ticks()
        
        # Assert
        assert result == ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA']
        mock_read_csv.assert_called_once_with(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv"
        )

    @patch('pandas.read_csv')
    def test_obtendo_ticks_empty_dataframe(self, mock_read_csv):
        """Testa a obtenção de tickers com DataFrame vazio."""
        # Arrange
        mock_df = pd.DataFrame({'tic': []})
        mock_read_csv.return_value = mock_df
        verificador = VerificadorTicks("PETR4.SA")
        
        # Act
        result = verificador.obtendo_ticks()
        
        # Assert
        assert result == []

    @patch.object(VerificadorTicks, 'obtendo_ticks')
    def test_verificando_ticks_true(self, mock_obtendo_ticks):
        """Testa verificação de ticker válido."""
        # Arrange
        mock_obtendo_ticks.return_value = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA']
        verificador = VerificadorTicks("PETR4.SA")
        
        # Act
        result = verificador.verificando_ticks()
        
        # Assert
        assert result is True

    @patch.object(VerificadorTicks, 'obtendo_ticks')
    def test_verificando_ticks_false(self, mock_obtendo_ticks):
        """Testa verificação de ticker inválido."""
        # Arrange
        mock_obtendo_ticks.return_value = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA']
        verificador = VerificadorTicks("INVALID.SA")
        
        # Act
        result = verificador.verificando_ticks()
        
        # Assert
        assert result is False

    @patch.object(VerificadorTicks, 'obtendo_ticks')
    def test_verificando_ticks_empty_list(self, mock_obtendo_ticks):
        """Testa verificação com lista vazia de tickers."""
        # Arrange
        mock_obtendo_ticks.return_value = []
        verificador = VerificadorTicks("PETR4.SA")
        
        # Act
        result = verificador.verificando_ticks()
        
        # Assert
        assert result is False

    @patch('pandas.read_csv')
    def test_verificando_ticks_integration(self, mock_read_csv):
        """Teste de integração para verificação de tickers."""
        # Arrange
        mock_df = pd.DataFrame({'tic': ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA']})
        mock_read_csv.return_value = mock_df
        
        # Test valid ticker
        verificador_valid = VerificadorTicks("PETR4.SA")
        assert verificador_valid.verificando_ticks() is True
        
        # Test invalid ticker
        verificador_invalid = VerificadorTicks("INVALID.SA")
        assert verificador_invalid.verificando_ticks() is False