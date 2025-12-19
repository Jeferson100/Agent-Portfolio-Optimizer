"""Testes para o módulo DataCache."""

import pytest
from unittest.mock import patch, Mock, MagicMock
import pandas as pd
from datetime import datetime
from portfolio_optimizer.coleta_dados.data_cache import DataCache


class TestDataCache:
    """Testes para a classe DataCache."""

    def test_init(self):
        """Testa a inicialização da classe."""
        cache = DataCache()
        assert cache.ticker_cache == {}
        assert cache.info_cache == {}
        assert cache.dividends_cache == {}
        assert cache.history_cache == {}
        assert cache.history_cache_dez_anos == {}
        assert cache.dowload_cache == {}
        assert cache.ipea_cache == {}
        assert cache.finances_cache == {}
        assert cache.balance_sheet_cache == {}
        assert cache.cash_flow_cache == {}
        assert cache.quarterly_balance_sheet_cache == {}
        assert cache.history_bovespa_cache == {}

    @patch('yfinance.Ticker')
    def test_get_ticker_new(self, mock_ticker_class):
        """Testa obtenção de novo ticker."""
        # Arrange
        mock_ticker_instance = Mock()
        mock_ticker_class.return_value = mock_ticker_instance
        cache = DataCache()
        
        # Act
        result = cache.get_ticker("PETR4.SA")
        
        # Assert
        assert result == mock_ticker_instance
        assert cache.ticker_cache["PETR4.SA"] == mock_ticker_instance
        mock_ticker_class.assert_called_once_with("PETR4.SA")

    def test_get_ticker_cached(self):
        """Testa obtenção de ticker já em cache."""
        # Arrange
        cache = DataCache()
        mock_ticker = Mock()
        cache.ticker_cache["PETR4.SA"] = mock_ticker
        
        # Act
        result = cache.get_ticker("PETR4.SA")
        
        # Assert
        assert result == mock_ticker

    @patch.object(DataCache, 'get_ticker')
    def test_get_info_new(self, mock_get_ticker):
        """Testa obtenção de novas informações."""
        # Arrange
        mock_ticker = Mock()
        mock_ticker.info = {"symbol": "PETR4.SA", "longName": "Petrobras"}
        mock_get_ticker.return_value = mock_ticker
        cache = DataCache()
        
        # Act
        result = cache.get_info("PETR4.SA")
        
        # Assert
        assert result == {"symbol": "PETR4.SA", "longName": "Petrobras"}
        assert cache.info_cache["PETR4.SA"] == {"symbol": "PETR4.SA", "longName": "Petrobras"}

    def test_get_info_cached(self):
        """Testa obtenção de informações já em cache."""
        # Arrange
        cache = DataCache()
        info_data = {"symbol": "PETR4.SA", "longName": "Petrobras"}
        cache.info_cache["PETR4.SA"] = info_data
        
        # Act
        result = cache.get_info("PETR4.SA")
        
        # Assert
        assert result == info_data

    @patch.object(DataCache, 'get_ticker')
    def test_get_dividends_new(self, mock_get_ticker):
        """Testa obtenção de novos dividendos."""
        # Arrange
        mock_ticker = Mock()
        dividends_data = pd.Series([0.5, 0.6, 0.7])
        mock_ticker.dividends = dividends_data
        mock_get_ticker.return_value = mock_ticker
        cache = DataCache()
        
        # Act
        result = cache.get_dividends("PETR4.SA")
        
        # Assert
        pd.testing.assert_series_equal(result, dividends_data)
        pd.testing.assert_series_equal(cache.dividends_cache["PETR4.SA"], dividends_data)

    @patch.object(DataCache, 'get_ticker')
    def test_get_history_new(self, mock_get_ticker):
        """Testa obtenção de novo histórico."""
        # Arrange
        mock_ticker = Mock()
        history_data = pd.DataFrame({'Close': [25.0, 25.5, 26.0]})
        mock_ticker.history.return_value = history_data
        mock_get_ticker.return_value = mock_ticker
        cache = DataCache()
        
        # Act
        result = cache.get_history("PETR4.SA", "1y")
        
        # Assert
        pd.testing.assert_frame_equal(result, history_data)
        mock_ticker.history.assert_called_once_with(period="1y")

    @patch.object(DataCache, 'get_ticker')
    def test_get_historical_dez_anos(self, mock_get_ticker):
        """Testa obtenção de histórico de 10 anos."""
        # Arrange
        mock_ticker = Mock()
        history_data = pd.DataFrame({'Close': [25.0, 25.5, 26.0]})
        mock_ticker.history.return_value = history_data
        mock_get_ticker.return_value = mock_ticker
        cache = DataCache()
        
        # Act
        result = cache.get_historical_dez_anos("PETR4.SA")
        
        # Assert
        pd.testing.assert_frame_equal(result, history_data)
        mock_ticker.history.assert_called_once_with(period="10Y", interval="1d")

    @patch('yfinance.download')
    @patch('portfolio_optimizer.coleta_dados.data_cache.datetime')
    def test_get_dowload(self, mock_datetime, mock_yf_download):
        """Testa download de dados."""
        # Arrange
        mock_datetime.today.return_value.strftime.return_value = "2023-12-31"
        download_data = pd.DataFrame({'Close': [25.0, 25.5, 26.0]})
        mock_yf_download.return_value = download_data
        cache = DataCache()
        
        # Act
        result = cache.get_dowload("PETR4.SA")
        
        # Assert
        pd.testing.assert_frame_equal(result, download_data)
        mock_yf_download.assert_called_once_with(
            "PETR4.SA", start="2004-01-01", end="2023-12-31"
        )

    @patch('yfinance.Ticker')
    def test_get_financials(self, mock_ticker_class):
        """Testa obtenção de dados financeiros."""
        # Arrange
        mock_ticker = Mock()
        financials_data = pd.DataFrame({'Revenue': [1000, 1100, 1200]})
        mock_ticker.get_financials.return_value = financials_data
        mock_ticker_class.return_value = mock_ticker
        cache = DataCache()
        
        # Act
        result = cache.get_financials("PETR4.SA")
        
        # Assert
        pd.testing.assert_frame_equal(result, financials_data)

    @patch('portfolio_optimizer.coleta_dados.data_cache.timeseries')
    def test_get_ipea_data(self, mock_timeseries):
        """Testa obtenção de dados do IPEA."""
        # Arrange
        ipea_data = pd.DataFrame({'value': [10.5, 10.6, 10.7]})
        mock_timeseries.return_value = ipea_data
        cache = DataCache()
        
        # Act
        result = cache.get_ipea_data("SERIES123")
        
        # Assert
        pd.testing.assert_frame_equal(result, ipea_data)
        mock_timeseries.assert_called_once_with("SERIES123")

    def test_clear_ticker_cache_specific(self):
        """Testa limpeza de cache específico de ticker."""
        # Arrange
        cache = DataCache()
        cache.ticker_cache = {"PETR4.SA": Mock(), "VALE3.SA": Mock()}
        
        # Act
        cache.clear_ticker_cache("PETR4.SA")
        
        # Assert
        assert "PETR4.SA" not in cache.ticker_cache
        assert "VALE3.SA" in cache.ticker_cache

    def test_clear_ticker_cache_all(self):
        """Testa limpeza de todo o cache de tickers."""
        # Arrange
        cache = DataCache()
        cache.ticker_cache = {"PETR4.SA": Mock(), "VALE3.SA": Mock()}
        
        # Act
        cache.clear_ticker_cache()
        
        # Assert
        assert cache.ticker_cache == {}

    def test_clear_all_cache(self):
        """Testa limpeza de todo o cache."""
        # Arrange
        cache = DataCache()
        cache.ticker_cache = {"PETR4.SA": Mock()}
        cache.info_cache = {"PETR4.SA": {}}
        cache.dividends_cache = {"PETR4.SA": pd.Series()}
        
        # Act
        cache.clear_all_cache()
        
        # Assert
        assert cache.ticker_cache == {}
        assert cache.info_cache == {}
        assert cache.dividends_cache == {}

    def test_get_cache_size(self):
        """Testa obtenção do tamanho do cache."""
        # Arrange
        cache = DataCache()
        cache.ticker_cache = {"PETR4.SA": Mock(), "VALE3.SA": Mock()}
        cache.info_cache = {"PETR4.SA": {}}
        
        # Act
        result = cache.get_cache_size()
        
        # Assert
        assert result["ticker_cache"] == 2
        assert result["info_cache"] == 1
        assert result["dividends_cache"] == 0

    @patch('yfinance.download')
    @patch('portfolio_optimizer.coleta_dados.data_cache.datetime')
    def test_get_history_bovespa(self, mock_datetime, mock_yf_download):
        """Testa obtenção do histórico da Bovespa."""
        # Arrange
        mock_datetime.today.return_value.strftime.return_value = "2023-12-31"
        bovespa_data = pd.DataFrame({'Close': [100000, 101000, 102000]})
        mock_yf_download.return_value = bovespa_data
        cache = DataCache()
        
        # Act
        result = cache.get_history_bovespa("2004-01-01", "2023-12-31")
        
        # Assert
        pd.testing.assert_frame_equal(result, bovespa_data)
        mock_yf_download.assert_called_once_with(
            "^BVSP", start="2004-01-01", end="2023-12-31"
        )