import asyncio
from typing import Any, List

import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

from ..coleta_dados import DadosIndicadoresTecnicos


class TratandoDadosIndicadoresComparacao:
    def __init__(
        self, tickers: List[str], periodo: str = "1Y", intervalo: str = "1wk"
    ) -> None:
        self.tickers = tickers
        self.periodo = periodo
        self.intervalo = intervalo

    async def coletando_indicadores(self, ticker: str) -> pd.DataFrame:
        ind_tecnicos = DadosIndicadoresTecnicos(
            ticker=ticker, periodo=self.periodo, intervalo=self.intervalo
        )
        return ind_tecnicos.pegando_indicadores_tecnicos()

    async def tratando_indicadores(self, ticker: str) -> pd.DataFrame:
        indicadores = await self.coletando_indicadores(ticker=ticker)
        indicadores = indicadores.reset_index()
        indicadores["Date"] = indicadores["Date"].dt.strftime("%Y-%m-%d")
        indicadores["tickers"] = ticker
        return indicadores

    async def indicadores_data_loader(self, ticker: str) -> List[Any]:
        dados = await self.tratando_indicadores(ticker=ticker)
        return DataFrameLoader(dados, page_content_column="Date").load()

    async def pegando_indicadores_comparacao(self):
        resutado_ticks = await asyncio.gather(
            *[self.indicadores_data_loader(ticker=ticker) for ticker in self.tickers]
        )

        return resutado_ticks
