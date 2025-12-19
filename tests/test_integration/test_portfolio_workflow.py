"""Testes de integração para o workflow completo do portfolio."""

import pytest
from unittest.mock import Mock, patch
from portfolio_optimizer.coleta_dados.verificador_ticks import VerificadorTicks
from portfolio_optimizer.coleta_dados.data_cache import DataCache
from portfolio_optimizer.utils.funcoes_utilitarias import normalizar_pesos


@pytest.mark.integration
class TestPortfolioWorkflow:
    """Testes de integração para o workflow completo."""

    @patch('pandas.read_csv')
    def test_verificacao_e_cache_workflow(self, mock_read_csv):
        """Testa workflow de verificação de tickers e cache."""
        # Arrange
        import pandas as pd
        mock_df = pd.DataFrame({'tic': ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA']})
        mock_read_csv.return_value = mock_df
        
        verificador = VerificadorTicks("PETR4.SA")
        cache = DataCache()
        
        # Act
        is_valid = verificador.verificando_ticks()
        
        # Assert
        assert is_valid is True
        assert len(cache.ticker_cache) == 0  # Cache ainda vazio

    def test_normalizacao_pesos_workflow(self):
        """Testa workflow de normalização de pesos."""
        # Arrange
        pesos_iniciais = {
            "PETR4.SA": 23.5,
            "VALE3.SA": 31.2,
            "ITUB4.SA": 19.8,
            "BBDC4.SA": 24.1
        }
        
        # Act
        pesos_normalizados = normalizar_pesos(pesos_iniciais)
        
        # Assert
        assert abs(sum(pesos_normalizados.values()) - 100.0) < 0.001
        assert len(pesos_normalizados) == 4
        assert all(peso > 0 for peso in pesos_normalizados.values())

    @patch('pandas.read_csv')
    def test_validacao_multiplos_tickers(self, mock_read_csv):
        """Testa validação de múltiplos tickers."""
        # Arrange
        import pandas as pd
        mock_df = pd.DataFrame({'tic': ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA']})
        mock_read_csv.return_value = mock_df
        
        tickers_para_testar = ['PETR4.SA', 'VALE3.SA', 'INVALID.SA', 'ITUB4.SA']
        
        # Act
        resultados = []
        for ticker in tickers_para_testar:
            verificador = VerificadorTicks(ticker)
            resultados.append((ticker, verificador.verificando_ticks()))
        
        # Assert
        assert resultados[0] == ('PETR4.SA', True)
        assert resultados[1] == ('VALE3.SA', True)
        assert resultados[2] == ('INVALID.SA', False)
        assert resultados[3] == ('ITUB4.SA', True)

    def test_cache_e_normalizacao_integrados(self):
        """Testa integração entre cache e normalização."""
        # Arrange
        cache = DataCache()
        pesos_desbalanceados = {
            "PETR4.SA": 22.0,
            "VALE3.SA": 33.0,
            "ITUB4.SA": 20.0,
            "BBDC4.SA": 23.5
        }
        
        # Simular dados no cache
        cache.info_cache["PETR4.SA"] = {"symbol": "PETR4.SA", "longName": "Petrobras"}
        cache.info_cache["VALE3.SA"] = {"symbol": "VALE3.SA", "longName": "Vale"}
        
        # Act
        pesos_normalizados = normalizar_pesos(pesos_desbalanceados)
        cache_size = cache.get_cache_size()
        
        # Assert
        assert abs(sum(pesos_normalizados.values()) - 100.0) < 0.001
        assert cache_size["info_cache"] == 2
        assert cache_size["ticker_cache"] == 0