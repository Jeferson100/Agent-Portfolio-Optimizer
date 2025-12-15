import warnings
from datetime import datetime
from typing import Dict

import pandas as pd
import sidrapy
import yfinance as yf

warnings.filterwarnings("ignore")


class VariacaoReceita:
    def __init__(self, ticker: str, deflacionar_receita: bool = True):
        self.stock = yf.Ticker(ticker=ticker)
        self.deflacionar_receita = deflacionar_receita

    def financials(self) -> pd.DataFrame:
        raw_financials = self.stock.get_financials(freq="yearly")
        if isinstance(raw_financials, pd.DataFrame):
            return raw_financials
        if isinstance(raw_financials, dict):
            return pd.DataFrame.from_dict(raw_financials)
        raise TypeError("Erro: Formato inesperado dos dados financeiros.")

    def pegando_inflacao(self) -> pd.DataFrame | None:
        ipca_raw = sidrapy.get_table(
            table_code="1737",
            territorial_level="1",
            ibge_territorial_code="all",
            variable="69",
            period="last%20472",
        )

        if ipca_raw is None:
            return None  # Retorno correto para None

        if isinstance(ipca_raw, dict):
            return pd.DataFrame.from_dict(ipca_raw)  # Converte para DataFrame

        if isinstance(ipca_raw, pd.DataFrame):
            return ipca_raw  # Retorna diretamente

        raise TypeError("Erro: Tipo de retorno inesperado.")

    def modificando_datas_inflacao(self) -> pd.DataFrame | None:
        ipca_raw = self.pegando_inflacao()
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

    def receita_passada_dataframe(self) -> pd.DataFrame:
        receita_passada = pd.DataFrame(self.financials().loc["TotalRevenue"].iloc[::-1])
        receita_passada["mes_ano"] = (
            pd.to_datetime(receita_passada.index).strftime("%Y-%m").values
        )
        return receita_passada

    def pegando_inflacao_datas_receita(self) -> pd.DataFrame:
        receita_inflacao = self.receita_passada_dataframe()
        ipca_mes = self.modificando_datas_inflacao()
        if (
            ipca_mes is not None
            and not pd.to_datetime(receita_inflacao.index).month.isin([6, 3, 9]).any()
        ):
            receita_inflacao["ipca"] = ipca_mes[
                ipca_mes["data_mes_ano"].isin(receita_inflacao["mes_ano"])
            ]["V"].values.astype(float)
            receita_inflacao["TotalRevenue"] = receita_inflacao["TotalRevenue"].astype(
                float
            )

            receita_inflacao.reset_index(inplace=True)
        return receita_inflacao

    def inflacao_acumulada(self, data: pd.DataFrame) -> pd.DataFrame:
        inflacao_acumu = data.copy()
        inflacao_acumu["inflacao_acumulada"] = (
            (1 + inflacao_acumu["ipca"].iloc[::-1].shift(1) / 100)
            .cumprod()
            .iloc[::-1]
            .values
        )
        inflacao_acumu.iloc[-1, -1] = 1
        return inflacao_acumu

    def deflacionando_receita(self, data: pd.DataFrame) -> pd.DataFrame:
        receita_deflacionada = data.copy()
        receita_deflacionada["TotalRevenueAjustado"] = (
            receita_deflacionada["TotalRevenue"]
            * receita_deflacionada["inflacao_acumulada"]
        )
        return receita_deflacionada

    def pct_receita_normal(self, data: pd.DataFrame) -> pd.DataFrame:
        pct_data_normal = data.copy()
        pct_data_normal["receita_pct"] = pct_data_normal["TotalRevenue"].pct_change()
        return pct_data_normal

    def pct_receita_deflacionada(self, data: pd.DataFrame) -> pd.DataFrame:
        pct_dat_deflacionada = data.copy()
        pct_dat_deflacionada["receita_pct_deflacionado"] = pct_dat_deflacionada[
            "TotalRevenueAjustado"
        ].pct_change()
        return pct_dat_deflacionada

    def receita_crescimento_metricas(self) -> Dict[str, float]:
        receita_crescimento = self.pegando_inflacao_datas_receita()

        return_porcentagens = {}

        if self.deflacionar_receita and "ipca" in receita_crescimento.columns:
            receita_crescimento_inflacao_acumulada = self.inflacao_acumulada(
                data=receita_crescimento
            )

            crescimento_deflacionando_receita = self.deflacionando_receita(
                receita_crescimento_inflacao_acumulada
            )

            pct_crescimento_receita_deflacionada = self.pct_receita_deflacionada(
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

        receita_crescimento = self.pct_receita_normal(receita_crescimento)

        return_porcentagens["mean_normal"] = receita_crescimento["receita_pct"].mean()
        return_porcentagens["median_normal"] = receita_crescimento[
            "receita_pct"
        ].median()

        return return_porcentagens
