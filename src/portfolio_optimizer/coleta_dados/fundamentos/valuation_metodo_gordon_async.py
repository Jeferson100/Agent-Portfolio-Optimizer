import asyncio
import warnings
from datetime import datetime
from typing import Any, Dict

import numpy as np
import pandas as pd
from pandas.core.series import Series

from ..data_cache import DataCache

warnings.filterwarnings("ignore")

data_cache = DataCache()


class ValuationModoloGordonAsync:
    def __init__(
        self,
        ticker: str,
        start_date_retorno: str = "2004-01-01",
        end_date_retorno: str = datetime.today().strftime("%Y-%m-%d"),
    ):
        self.ticker = ticker
        self.data_cache = data_cache
        self.start_date_retorno = start_date_retorno
        self.end_date_retorno = end_date_retorno
        self.dicionario_indicadores: dict[str, Any] = {}
        self.dicionario_indicadores["ticker"] = ticker

    async def preco_historico(self) -> Series:  # type: ignore[type-arg]
        preco_his = self.data_cache.get_historical_dez_anos(self.ticker)["Close"]
        if preco_his is None:
            return pd.Series(dtype=float)
        if not isinstance(preco_his, pd.Series):  # Garante que é uma Series
            raise TypeError("Erro: 'Close' não retornou uma Series!")
        return preco_his.astype(float)

    async def g_sustainable(self) -> float:
        instanciando_funcao = self.data_cache.get_info(self.ticker)
        try:
            returnOnEquity = instanciando_funcao["returnOnEquity"]
        except KeyError:
            print("Nao tem returnOnEquity")
            returnOnEquity = 0
        try:
            payoutRatio = instanciando_funcao["payoutRatio"]
        except KeyError:
            print("Nao tem payoutRatio")
            payoutRatio = 0

        g_sust = returnOnEquity * (1 - payoutRatio)

        self.dicionario_indicadores["g_sust"] = round(g_sust, 4)

        return float(g_sust)

    async def beta(self) -> float:
        instanciando_funcao = self.data_cache.get_info(self.ticker)
        try:
            beta_acao = round(instanciando_funcao["beta"], 4)
        except KeyError:
            print("Nao tem beta")
            beta_acao = 1
        self.dicionario_indicadores["beta"] = beta_acao
        return float(beta_acao)

    async def juros_livre(self) -> float:
        juros = (
            self.data_cache.get_ipea_data("BMF12_SWAPDI36012")
            .rename(columns={"VALUE ((% a.a.))": "swaps"})[["swaps"]]
            .div(100)
            .iloc[-1]
            .swaps
        )
        self.dicionario_indicadores["juros_livre"] = round(juros, 4)
        return float(juros)

    async def retorno_mercado(self) -> float:
        ibov = self.data_cache.get_history_bovespa(
            start=self.start_date_retorno, end=self.end_date_retorno
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

    async def capm_gordon(self) -> float:
        juros, beta, retorno_mercado, juros_livre = await asyncio.gather(
            self.juros_livre(), self.beta(), self.retorno_mercado(), self.juros_livre()
        )

        wacc = juros + beta * (retorno_mercado - juros_livre)

        self.dicionario_indicadores["capm"] = float(round(wacc, 4))
        return wacc

    async def dividendos(self) -> Series:  # type: ignore[type-arg]
        """Retorna os dividendos da ação"""
        divi = self.data_cache.get_dividends(self.ticker)
        if divi is None:
            return pd.Series(dtype=float)
        if not isinstance(divi, pd.Series):  # Garante que é uma Series
            raise TypeError("Erro: 'Close' não retornou uma Series!")
        return divi.astype(float)

    async def anual_dividendo(self) -> pd.DataFrame:
        anual_dividendo = (
            pd.DataFrame(await self.dividendos())
            .tz_localize(None)
            .assign(Year=lambda x: x.index.year)
            .groupby(["Year"])
            .agg({"Dividends": "sum"})
            .iloc[:-1]
        )
        return anual_dividendo

    async def d1(self) -> float:
        instanciando_funcao = await self.anual_dividendo()
        dividendo = instanciando_funcao.median().Dividends
        self.dicionario_indicadores["dividendo_mediano"] = round(dividendo, 3)
        return float(dividendo)

    async def preco_acao(self) -> Dict[str, str]:
        d1_valor, capm, g_sust, preco_hist = await asyncio.gather(
            self.d1(), self.capm_gordon(), self.g_sustainable(), self.preco_historico()
        )

        pv = d1_valor / (capm - g_sust)

        preco_atual = preco_hist.values[-1]

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
