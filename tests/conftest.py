"""Configurações compartilhadas para os testes."""

import pytest
from unittest.mock import Mock, patch
import pandas as pd
import yfinance as yf


@pytest.fixture
def mock_ticker_data():
    """Mock de dados de ticker para testes."""
    return {
        'symbol': 'PETR4.SA',
        'longName': 'Petróleo Brasileiro S.A. - Petrobras',
        'sector': 'Energy',
        'industry': 'Oil & Gas Integrated',
        'marketCap': 500000000000,
        'currentPrice': 25.50
    }


@pytest.fixture
def mock_historical_data():
    """Mock de dados históricos para testes."""
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    return pd.DataFrame({
        'Open': [25.0 + i * 0.1 for i in range(100)],
        'High': [25.5 + i * 0.1 for i in range(100)],
        'Low': [24.5 + i * 0.1 for i in range(100)],
        'Close': [25.2 + i * 0.1 for i in range(100)],
        'Volume': [1000000 + i * 1000 for i in range(100)]
    }, index=dates)


@pytest.fixture
def mock_dividends_data():
    """Mock de dados de dividendos para testes."""
    dates = pd.date_range('2023-01-01', periods=4, freq='Q')
    return pd.Series([0.5, 0.6, 0.7, 0.8], index=dates)


@pytest.fixture
def sample_tickers():
    """Lista de tickers para testes."""
    return ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA']


@pytest.fixture
def mock_yfinance():
    """Mock do yfinance para evitar chamadas reais à API."""
    with patch('yfinance.Ticker') as mock_ticker:
        mock_instance = Mock()
        mock_ticker.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_pandas_read_csv():
    """Mock do pandas read_csv para testes."""
    with patch('pandas.read_csv') as mock_read:
        yield mock_read


@pytest.fixture
def sample_weights_dict():
    """Dicionário de pesos para testes."""
    return {
        'PETR4.SA': 25.0,
        'VALE3.SA': 30.0,
        'ITUB4.SA': 20.0,
        'BBDC4.SA': 25.0
    }


@pytest.fixture
def sample_unbalanced_weights():
    """Dicionário de pesos desbalanceados para testes."""
    return {
        'PETR4.SA': 23.5,
        'VALE3.SA': 31.2,
        'ITUB4.SA': 19.8,
        'BBDC4.SA': 24.1
    }


@pytest.fixture
def mock_llm_response():
    """Mock de resposta do LLM para testes."""
    return {
        "tickers_weights": {"PETR4.SA": 40.0, "VALE3.SA": 35.0, "ITUB4.SA": 25.0},
        "justification": "Diversificação entre setores com foco em commodities e bancos."
    }


@pytest.fixture
def mock_state_carteira():
    """Mock de state para criador de carteira."""
    return {
        "tickers_weights": {"PETR4.SA": 50.0, "VALE3.SA": 50.0},
        "justification": "Diversificação balanceada",
        "analise_avaliador_weights": "",
        "avaliacao_acoes": "Análise das ações",
        "correlacao_acoes": "Matriz de correlação",
        "interacao": 1,
        "soma_weights_error": None,
        "tics": ["PETR4.SA", "VALE3.SA", "ITUB4.SA"],
        "tics_error": ""
    }


@pytest.fixture
def mock_state_classification():
    """Mock de state para classificação de tics."""
    return {
        "tics": ["PETR4.SA", "VALE3.SA"],
        "dados_fundamentalistas": {"PETR4.SA": {"pe_ratio": 8.5}, "VALE3.SA": {"pe_ratio": 6.2}},
        "analysis": {"PETR4.SA": "BUY", "VALE3.SA": "HOLD"},
        "classification": {"PETR4.SA": "BUY", "VALE3.SA": "HOLD"},
        "interacao": 1
    }


@pytest.fixture
def mock_async_llm_router():
    """Mock assíncrono do LlmRouter."""
    mock = Mock()
    mock.llm_router = AsyncMock(return_value="mocked response")
    return mock


@pytest.fixture
def mock_structured_output_response():
    """Mock de resposta estruturada do LLM."""
    return {
        "result": "success",
        "confidence": 0.95,
        "data": {"key": "value"}
    }