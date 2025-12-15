import asyncio
import warnings

import pandas as pd

from ..data_cache import DataCache

warnings.filterwarnings("ignore")

data_cache = DataCache()


class PassivoTotalMenosDividaAsync:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.cache = data_cache

    async def passivo_nao_circulante(self) -> float:
        passivo_nao_circulante = self.cache.get_balance_sheet(self.ticker)
        if isinstance(passivo_nao_circulante, pd.DataFrame):
            if (
                "TotalNonCurrentLiabilitiesNetMinorityInterest"
                in passivo_nao_circulante.index
            ):
                out_terrenos = passivo_nao_circulante.loc[
                    "TotalNonCurrentLiabilitiesNetMinorityInterest"
                ][0]
            else:
                out_terrenos = 0
            if isinstance(out_terrenos, pd.Series):
                return float(out_terrenos.iloc[0])
            return float(out_terrenos)
        return 0.0

    async def passivos_circulante(self) -> float:
        passivo_circulante = self.cache.get_balance_sheet(self.ticker)
        if isinstance(passivo_circulante, pd.DataFrame):
            if "CurrentLiabilities" in passivo_circulante.index:
                out_terrenos = passivo_circulante.loc["CurrentLiabilities"][0]
            else:
                out_terrenos = 0
            if isinstance(out_terrenos, pd.Series):
                return float(out_terrenos.iloc[0])
            return float(out_terrenos)
        return 0.0

    async def divida_total(self) -> float:
        divida_total = self.cache.get_balance_sheet(self.ticker)
        if isinstance(divida_total, pd.DataFrame):
            if "TotalDebt" in divida_total.index:
                divida_total = divida_total.loc["TotalDebt"][0]
            else:
                divida_total = 0
            if isinstance(divida_total, pd.Series):
                return float(divida_total.iloc[0])
            return float(divida_total)
        return 0.0

    async def valor_total_passivo_menos_divida(self) -> float:
        # Executar as três funções em paralelo usando asyncio.gather
        divida_total, passivo_circulante, passivo_nao_circulante = await asyncio.gather(
            self.divida_total(),
            self.passivos_circulante(),
            self.passivo_nao_circulante(),
        )
        return passivo_circulante + passivo_nao_circulante - divida_total
