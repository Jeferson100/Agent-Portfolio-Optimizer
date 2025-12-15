from datetime import datetime
from functools import lru_cache

import yfinance as yf
from ipeadatapy import timeseries


class DataCache:
    """Gerenciador de cache para dados financeiros."""

    def __init__(self):
        self.ticker_cache = {}
        self.info_cache = {}
        self.dividends_cache = {}
        self.history_cache = {}
        self.history_cache_dez_anos = {}
        self.dowload_cache = {}
        self.ipea_cache = {}
        self.finances_cache = {}
        self.balance_sheet_cache = {}
        self.cash_flow_cache = {}
        self.quarterly_balance_sheet_cache = {}
        self.history_bovespa_cache = {}

    def get_ticker(self, ticker_symbol):
        """Obtém objeto Ticker com cache."""
        if ticker_symbol not in self.ticker_cache:
            self.ticker_cache[ticker_symbol] = yf.Ticker(ticker_symbol)
        return self.ticker_cache[ticker_symbol]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_info(self, ticker_symbol):
        """Obtém informações do ticker com cache."""
        if ticker_symbol not in self.info_cache:
            ticker = self.get_ticker(ticker_symbol)
            self.info_cache[ticker_symbol] = ticker.info
        return self.info_cache[ticker_symbol]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_dividends(self, ticker_symbol):
        """Obtém dividendos com cache."""
        if ticker_symbol not in self.dividends_cache:
            ticker = self.get_ticker(ticker_symbol)
            self.dividends_cache[ticker_symbol] = ticker.dividends
        return self.dividends_cache[ticker_symbol]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_history(self, ticker_symbol, period="1y"):
        """Obtém histórico de preços com cache."""
        cache_key = f"{ticker_symbol}_{period}"
        if cache_key not in self.history_cache:
            ticker = self.get_ticker(ticker_symbol)
            self.history_cache[cache_key] = ticker.history(period=period)
        return self.history_cache[cache_key]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_historical_dez_anos(self, ticker_symbol):
        """Obtém histórico de preços com cache."""
        cache_key = f"{ticker_symbol}_dez_anos"
        if cache_key not in self.history_cache_dez_anos:
            ticker = self.get_ticker(ticker_symbol)
            self.history_cache_dez_anos[cache_key] = ticker.history(
                period="10Y", interval="1d"
            )
        return self.history_cache_dez_anos[cache_key]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_dowload(self, ticker_symbol):
        "Obtem dowload dos dados"
        if ticker_symbol not in self.dowload_cache:
            self.dowload_cache[ticker_symbol] = yf.download(
                ticker_symbol,
                start="2004-01-01",
                end=datetime.today().strftime("%Y-%m-%d"),
            )
        return self.dowload_cache[ticker_symbol]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_financials(self, ticker_symbol):
        "Obtem dowload dos dados fincanceiros"
        if ticker_symbol not in self.finances_cache:
            self.finances_cache[ticker_symbol] = yf.Ticker(
                ticker_symbol
            ).get_financials()
        return self.finances_cache[ticker_symbol]

    @lru_cache(maxsize=10)  # noqa: B019
    def get_ipea_data(self, series_code):
        """Obtém dados do IPEA com cache."""
        if series_code not in self.ipea_cache:
            self.ipea_cache[series_code] = timeseries(series_code)
        return self.ipea_cache[series_code]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_balance_sheet(self, ticker_symbol):
        """ "Obtem dados do balanco"""
        if ticker_symbol not in self.balance_sheet_cache:
            self.balance_sheet_cache[ticker_symbol] = yf.Ticker(
                ticker_symbol
            ).get_balancesheet(freq="yearly")
        return self.balance_sheet_cache[ticker_symbol]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_cash_flow(self, ticker_symbol):
        """Obtem dados do fluxo de caixa"""
        if ticker_symbol not in self.cash_flow_cache:
            self.cash_flow_cache[ticker_symbol] = yf.Ticker(ticker_symbol).cashflow
        return self.cash_flow_cache[ticker_symbol]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_quarterly_balance_sheet(self, ticker_symbol):
        if ticker_symbol not in self.quarterly_balance_sheet_cache:
            self.quarterly_balance_sheet_cache[ticker_symbol] = yf.Ticker(
                ticker_symbol
            ).quarterly_balance_sheet
        return self.quarterly_balance_sheet_cache[ticker_symbol]

    @lru_cache(maxsize=100)  # noqa: B019
    def get_history_bovespa(self, start, end):
        """Obtém histórico do índice Bovespa com cache."""
        cache_key = f"bovespa_{start}_{end}"
        if cache_key not in self.history_bovespa_cache:
            self.history_bovespa_cache[cache_key] = yf.download(
                "^BVSP", start="2004-01-01", end=datetime.today().strftime("%Y-%m-%d")
            )
        return self.history_bovespa_cache[cache_key]

    def clear_history_bovespa_cache(self):
        """Limpa o cache do histórico do índice Bovespa."""
        self.get_history_bovespa.cache_clear()
        self.history_bovespa_cache.clear()

    def clear_history_cache_dez_anos(self, ticker_symbol=None):
        self.get_historical_dez_anos.cache_clear()
        if ticker_symbol:
            self.history_cache_dez_anos.pop(ticker_symbol, None)
        else:
            self.history_cache_dez_anos.clear()

    def clear_quarterly_balance_sheet_cache(self, ticker_symbol=None):
        self.get_quarterly_balance_sheet.cache_clear()
        if ticker_symbol:
            self.balance_sheet_cache.pop(ticker_symbol, None)
        else:
            self.balance_sheet_cache.clear()

    def clear_cash_flow_cache(self, ticker_symbol=None):
        """Limpa o cache de fluxo de caixa de um ticker específico ou todo o cache."""
        self.get_cash_flow.cache_clear()
        if ticker_symbol:
            self.balance_sheet_cache.pop(ticker_symbol, None)
        else:
            self.balance_sheet_cache.clear()

    def clear_ticker_cache(self, ticker_symbol=None):
        """Limpa o cache de um ticker específico ou todo o cache de tickers."""
        if ticker_symbol:
            self.ticker_cache.pop(ticker_symbol, None)
        else:
            self.ticker_cache.clear()

    def clear_info_cache(self, ticker_symbol=None):
        """Limpa o cache de informações de um ticker específico ou todo o cache."""
        self.get_info.cache_clear()  # Limpa o cache do decorador lru_cache
        if ticker_symbol:
            self.info_cache.pop(ticker_symbol, None)
        else:
            self.info_cache.clear()

    def clear_dividends_cache(self, ticker_symbol=None):
        """Limpa o cache de dividendos de um ticker específico ou todo o cache."""
        self.get_dividends.cache_clear()
        if ticker_symbol:
            self.dividends_cache.pop(ticker_symbol, None)
        else:
            self.dividends_cache.clear()

    def clear_history_cache(self, ticker_symbol=None):
        """Limpa o cache de histórico de um ticker específico ou todo o cache."""
        self.get_history.cache_clear()
        if ticker_symbol:
            keys_to_remove = [
                k for k in self.history_cache.keys() if k.startswith(ticker_symbol)
            ]
            for k in keys_to_remove:
                self.history_cache.pop(k, None)
        else:
            self.history_cache.clear()

    def clear_download_cache(self, ticker_symbol=None):
        """Limpa o cache de downloads de um ticker específico ou todo o cache."""
        self.get_dowload.cache_clear()
        if ticker_symbol:
            self.dowload_cache.pop(ticker_symbol, None)
        else:
            self.dowload_cache.clear()

    def clear_financials_cache(self, ticker_symbol=None):
        """Limpa o cache de dados financeiros de um ticker específico ou todo o cache."""
        self.get_financials.cache_clear()
        if ticker_symbol:
            self.finances_cache.pop(ticker_symbol, None)
        else:
            self.finances_cache.clear()

    def clear_ipea_cache(self, series_code=None):
        """Limpa o cache de dados do IPEA de uma série específica ou todo o cache."""
        self.get_ipea_data.cache_clear()
        if series_code:
            self.ipea_cache.pop(series_code, None)
        else:
            self.ipea_cache.clear()

    def clear_get_balance_sheet(self, ticker_symbol=None):
        """Limpa o cache de balanco de um ticker específico ou todo o cache."""
        self.get_balance_sheet.cache_clear()
        if ticker_symbol:
            self.balance_sheet_cache.pop(ticker_symbol, None)
        else:
            self.balance_sheet_cache.clear()

    def clear_all_cache(self):
        """Limpa todo o cache."""
        self.clear_ticker_cache()
        self.clear_info_cache()
        self.clear_dividends_cache()
        self.clear_history_cache()
        self.clear_download_cache()
        self.clear_financials_cache()
        self.clear_ipea_cache()
        self.clear_get_balance_sheet()
        self.clear_cash_flow_cache()
        self.clear_quarterly_balance_sheet_cache()
        self.clear_history_cache_dez_anos()
        self.clear_history_bovespa_cache()

    def get_cache_size(self):
        """Retorna o tamanho atual de cada cache."""
        return {
            "ticker_cache": len(self.ticker_cache),
            "info_cache": len(self.info_cache),
            "dividends_cache": len(self.dividends_cache),
            "history_cache": len(self.history_cache),
            "download_cache": len(self.dowload_cache),
            "financials_cache": len(self.finances_cache),
            "ipea_cache": len(self.ipea_cache),
            "balance_sheet": len(self.balance_sheet_cache),
            "cash_flow": len(self.balance_sheet_cache),
            "quarterly_balance_sheet": len(self.balance_sheet_cache),
            "history_cache_dez_anos": len(self.history_cache_dez_anos),
            "history_bovespa_cache": len(self.history_bovespa_cache),
        }
