import asyncio
import warnings
from datetime import datetime
from typing import Dict

import aiohttp
import pandas as pd
import sidrapy

from ..data_cache import DataCache

warnings.filterwarnings("ignore")

data_cache = DataCache()


class VariacaoReceitaAsync:
    def __init__(self, ticker: str, deflacionar_receita: bool = True):
        self.ticker = ticker
        self.data_cache = data_cache
        self.deflacionar_receita = deflacionar_receita

    async def financials(self) -> pd.DataFrame:
        raw_financials = self.data_cache.get_financials(self.ticker)
        if isinstance(raw_financials, pd.DataFrame):
            return raw_financials
        if isinstance(raw_financials, dict):
            return pd.DataFrame.from_dict(raw_financials)
        raise TypeError("Erro: Formato inesperado dos dados financeiros.")

    async def pegando_inflacao(self) -> pd.DataFrame | None:
        async with aiohttp.ClientSession() as _:  # pylint: disable=consider-using-with
            ipca_raw = await asyncio.to_thread(
                sidrapy.get_table,
                table_code="1737",
                territorial_level="1",
                ibge_territorial_code="all",
                variable="69",
                period="last%20472",
            )

            if ipca_raw is None:
                return None

            if isinstance(ipca_raw, dict):
                return pd.DataFrame.from_dict(ipca_raw)

            if isinstance(ipca_raw, pd.DataFrame):
                return ipca_raw

            raise TypeError("Erro: Tipo de retorno inesperado.")

    async def modificando_datas_inflacao(self) -> pd.DataFrame | None:
        ipca_raw = await self.pegando_inflacao()
        if isinstance(ipca_raw, pd.DataFrame):
            ipca_raw = ipca_raw.iloc[1:]
        if ipca_raw is None:
            return None
        ipca_raw.loc[:, "data"] = ipca_raw["D2C"].apply(
            lambda x: datetime.strptime(str(x), "%Y%m")
        )
        ipca_mes_doze = ipca_raw[ipca_raw["data"].dt.month == 12]
        ipca_mes_doze.loc[:, "data_mes_ano"] = pd.to_datetime(
            ipca_mes_doze["data"]
        ).dt.strftime("%Y-%m")
        return ipca_mes_doze

    async def receita_passada_dataframe(self) -> pd.DataFrame:
        financials = await self.financials()
        receita_passada = pd.DataFrame(financials.loc["TotalRevenue"].iloc[::-1])
        receita_passada["mes_ano"] = (
            pd.to_datetime(receita_passada.index).strftime("%Y-%m").values
        )
        return receita_passada

    async def pegando_inflacao_datas_receita(self) -> pd.DataFrame:
        receita_passada, ipca_mes = await asyncio.gather(
            self.receita_passada_dataframe(), self.modificando_datas_inflacao()
        )

        if (
            ipca_mes is not None
            and not pd.to_datetime(receita_passada.index).month.isin([6, 3, 9]).any()
        ):
            receita_passada["ipca"] = ipca_mes[
                ipca_mes["data_mes_ano"].isin(receita_passada["mes_ano"])
            ]["V"].values.astype(float)
            receita_passada["TotalRevenue"] = receita_passada["TotalRevenue"].astype(
                float
            )

            receita_passada.reset_index(inplace=True)
        return receita_passada

    async def inflacao_acumulada(self, data: pd.DataFrame) -> pd.DataFrame:
        inflacao_acumu = data.copy()
        inflacao_acumu["inflacao_acumulada"] = (
            (1 + inflacao_acumu["ipca"].iloc[::-1].shift(1) / 100)
            .cumprod()
            .iloc[::-1]
            .values
        )
        inflacao_acumu.iloc[-1, -1] = 1
        return inflacao_acumu

    async def deflacionando_receita(self, data: pd.DataFrame) -> pd.DataFrame:
        receita_deflacionada = data.copy()
        receita_deflacionada["TotalRevenueAjustado"] = (
            receita_deflacionada["TotalRevenue"]
            * receita_deflacionada["inflacao_acumulada"]
        )
        return receita_deflacionada

    async def pct_receita_normal(self, data: pd.DataFrame) -> pd.DataFrame:
        pct_data_normal = data.copy()
        pct_data_normal["receita_pct"] = pct_data_normal["TotalRevenue"].pct_change()
        return pct_data_normal

    async def pct_receita_deflacionada(self, data: pd.DataFrame) -> pd.DataFrame:
        pct_dat_deflacionada = data.copy()
        pct_dat_deflacionada["receita_pct_deflacionado"] = pct_dat_deflacionada[
            "TotalRevenueAjustado"
        ].pct_change()
        return pct_dat_deflacionada

    async def receita_crescimento_metricas(self) -> Dict[str, float]:
        receita_crescimento = await self.pegando_inflacao_datas_receita()

        return_porcentagens = {}

        if self.deflacionar_receita and "ipca" in receita_crescimento.columns:
            receita_crescimento_inflacao_acumulada = self.inflacao_acumulada(
                data=receita_crescimento
            )

            crescimento_deflacionando_receita = await self.deflacionando_receita(
                await receita_crescimento_inflacao_acumulada
            )

            pct_crescimento_receita_deflacionada = await self.pct_receita_deflacionada(
                crescimento_deflacionando_receita
            )

            receita_crescimento = pct_crescimento_receita_deflacionada.copy()

            return_porcentagens["mean_deflacionada"] = (
                pct_crescimento_receita_deflacionada["receita_pct_deflacionado"].mean()
            )
            return_porcentagens["median_deflacionada"] = (
                pct_crescimento_receita_deflacionada[
                    "receita_pct_deflacionado"
                ].median()
            )

        receita_crescimento = await self.pct_receita_normal(receita_crescimento)

        return_porcentagens["mean_normal"] = receita_crescimento["receita_pct"].mean()
        return_porcentagens["median_normal"] = receita_crescimento[
            "receita_pct"
        ].median()

        return return_porcentagens
