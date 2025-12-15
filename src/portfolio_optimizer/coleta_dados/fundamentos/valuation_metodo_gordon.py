import warnings
from datetime import datetime
from typing import Any, Dict

import ipeadatapy as ip
import numpy as np
import pandas as pd
import yfinance as yf
from pandas.core.series import Series

warnings.filterwarnings("ignore")


class ValuationModoloGordon:
    def __init__(
        self,
        ticker: str,
        start_date_retorno: str = "2004-01-01",
        end_date_retorno: str = datetime.today().strftime("%Y-%m-%d"),
    ):
        self.ticker = ticker
        self.start_date_retorno = start_date_retorno
        self.end_date_retorno = end_date_retorno
        self.dicionario_indicadores: dict[str, Any] = {}
        self.dicionario_indicadores["ticker"] = ticker

    def acao(self) -> yf.Ticker:
        setando_ticker = yf.Ticker(self.ticker)
        setando_ticker.history(period="10Y", interval="1d")
        return setando_ticker

    def preco_historico(self) -> Series:  # type: ignore[type-arg]
        preco_his = self.acao().history(period="10Y", interval="1d")["Close"]
        if preco_his is None:
            return pd.Series(dtype=float)
        if not isinstance(preco_his, pd.Series):  # Garante que é uma Series
            raise TypeError("Erro: 'Close' não retornou uma Series!")
        return preco_his.astype(float)

    def g_sustainable(self) -> float:
        try:
            returnOnEquity = self.acao().info["returnOnEquity"]
        except KeyError:
            print("Nao tem returnOnEquity")
            returnOnEquity = 0
        try:
            payoutRatio = self.acao().get_info()["payoutRatio"]
        except KeyError:
            print("Nao tem payoutRatio")
            payoutRatio = 0

        g_sust = returnOnEquity * (1 - payoutRatio)

        self.dicionario_indicadores["g_sust"] = round(g_sust, 4)

        return float(g_sust)

    def beta(self) -> float:
        try:
            beta_acao = round(self.acao().info["beta"], 4)
        except KeyError:
            print("Nao tem beta")
            beta_acao = 1
        self.dicionario_indicadores["beta"] = beta_acao
        return float(beta_acao)

    def juros_livre(self) -> float:
        juros = (
            ip.timeseries("BMF12_SWAPDI36012")  # type: ignore
            .rename(columns={"VALUE ((% a.a.))": "swaps"})[["swaps"]]
            .div(100)
            .iloc[-1]
            .swaps
        )
        self.dicionario_indicadores["juros_livre"] = round(juros, 4)
        return float(juros)

    def retorno_mercado(self) -> float:
        ibov = yf.download(
            "^BVSP", start=self.start_date_retorno, end=self.end_date_retorno
        )
        if ibov is None or ibov.empty:
            raise ValueError("Erro: Nenhum dado foi baixado para o IBOVESPA.")

        # Garantir que a coluna 'Close' existe
        if "Close" not in ibov.columns:
            raise ValueError("Erro: A coluna 'Close' não está presente nos dados.")

        porcentagem = ibov.pct_change()["Close"]

        porcentagem.dropna(axis=0, inplace=True)

        compounded_growth = (1 + porcentagem).prod()

        n_periods = porcentagem.shape[0]

        retorno_medio = compounded_growth ** (252 / n_periods) - 1

        return float(retorno_medio["^BVSP"])

    def capm_gordon(self) -> float:
        wacc = self.juros_livre() + self.beta() * (
            self.retorno_mercado() - self.juros_livre()
        )
        self.dicionario_indicadores["capm"] = float(round(wacc, 4))
        return wacc

    def dividendos(self) -> Series:  # type: ignore[type-arg]
        divi = self.acao().dividends
        if divi is None:
            return pd.Series(dtype=float)
        if not isinstance(divi, pd.Series):  # Garante que é uma Series
            raise TypeError("Erro: 'Close' não retornou uma Series!")
        return divi.astype(float)

    def anual_dividendo(self) -> pd.DataFrame:
        anual_dividendo = (
            pd.DataFrame(self.dividendos())
            .tz_localize(None)
            .assign(Year=lambda x: x.index.year)
            .groupby(["Year"])
            .agg({"Dividends": "sum"})
            .iloc[:-1]
        )
        return anual_dividendo

    def d1(self) -> float:
        dividendo = self.anual_dividendo().median().Dividends
        self.dicionario_indicadores["dividendo_mediano"] = round(dividendo, 3)
        return float(dividendo)

    def preco_acao(self) -> Dict[str, str]:
        pv = self.d1() / (self.capm_gordon() - self.g_sustainable())

        preco_atual = self.preco_historico().values[-1]

        self.dicionario_indicadores["valuation_acao"] = round(pv, 2)

        self.dicionario_indicadores["preco_atual"] = round(preco_atual, 2)
        try:
            self.dicionario_indicadores["diferenca"] = round(
                ((pv - preco_atual) / preco_atual) * 100, 2
            )
        except ValueError:
            self.dicionario_indicadores["diferenca"] = "NaN"
        try:
            print(
                f"Diferença entre valuation e cotação: {((pv - preco_atual) / preco_atual) * 100:.2f}%"
            )
        except ValueError:
            print("Sem diferenca")
        if not np.isnan(pv):
            pv = round(pv)
        else:
            pv = 0
        return self.dicionario_indicadores
