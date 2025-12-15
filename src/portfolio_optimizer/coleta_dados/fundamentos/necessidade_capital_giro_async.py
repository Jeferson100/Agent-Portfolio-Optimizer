import asyncio
import math
import warnings

import pandas as pd

from ..data_cache import DataCache

warnings.filterwarnings("ignore")

data_cache = DataCache()


class NecessidadeCapitalGiroAsync:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.cache = data_cache

    async def get_balance_sheet(self) -> pd.DataFrame:
        return self.cache.get_balance_sheet(self.ticker)

    async def contas_receber(self) -> float:
        contas_receber = await self.get_balance_sheet()
        if isinstance(contas_receber, pd.DataFrame):
            if "AccountsReceivable" in contas_receber.index:
                contas_receber = contas_receber.loc["AccountsReceivable"][0]
            else:
                contas_receber = 0
            if isinstance(contas_receber, pd.Series):
                return float(contas_receber.iloc[0])
            return float(contas_receber)
        return 0.0

    async def estoque(self) -> float:
        estoque = await self.get_balance_sheet()
        if isinstance(estoque, pd.DataFrame):
            if "Inventory" in estoque.index:
                estoque = estoque.loc["Inventory"][0]
            else:
                estoque = 0
            if isinstance(estoque, pd.Series):
                return float(estoque.iloc[0])
            return float(estoque)
        return 0.0

    async def outros_ativos_circulantes_operacionais(self) -> float:
        outros_ativos = await self.get_balance_sheet()
        if isinstance(outros_ativos, pd.DataFrame):
            if "OtherCurrentAssets" in outros_ativos.index:
                outros_ativos = outros_ativos.loc["OtherCurrentAssets"][0]
            else:
                outros_ativos = 0
            if isinstance(outros_ativos, pd.Series):
                return float(outros_ativos.iloc[0])
            return float(outros_ativos)
        return 0.0

    async def outros_passivos_circulantes_operacionais(self) -> float:
        outros_passivo = await self.get_balance_sheet()
        if isinstance(outros_passivo, pd.DataFrame):
            if "OtherCurrentLiabilities" in outros_passivo.index:
                outros_passivo = outros_passivo.loc["OtherCurrentLiabilities"][0]
            else:
                outros_passivo = 0
            if isinstance(outros_passivo, pd.Series):
                return float(outros_passivo.iloc[0])
            return float(outros_passivo)
        return 0.0

    async def contas_pagar_despesas_acumuladas(self) -> float:
        contas_pagar = await self.get_balance_sheet()
        if isinstance(contas_pagar, pd.DataFrame):
            if "PayablesAndAccruedExpenses" in contas_pagar.index:
                contas_pagar = contas_pagar.loc["PayablesAndAccruedExpenses"][0]
            elif "AccountsPayable" in contas_pagar.index:
                contas_pagar = contas_pagar.loc["AccountsPayable"][0]
            elif "Payables" in contas_pagar.index:
                contas_pagar = contas_pagar.loc["Payables"][0]
            else:
                contas_pagar = 0
            if isinstance(contas_pagar, pd.Series):
                return float(contas_pagar.iloc[0])
            return float(contas_pagar)
        return 0.0

    async def ativos_circulantes_operacionais(self) -> float:
        contas_recebe, estoques, outros_ativos = await asyncio.gather(
            self.contas_receber(),
            self.estoque(),
            self.outros_ativos_circulantes_operacionais(),
        )

        if math.isnan(contas_recebe):
            contas_recebe = 0
        if math.isnan(estoques):
            estoques = 0
        if math.isnan(outros_ativos):
            outros_ativos = 0
        return contas_recebe + estoques + outros_ativos

    async def passivos_circulantes_operacionais(self) -> float:
        contas_pagar, outros_passivos = await asyncio.gather(
            self.contas_pagar_despesas_acumuladas(),
            self.outros_passivos_circulantes_operacionais(),
        )
        if math.isnan(contas_pagar):
            contas_pagar = 0
        if math.isnan(outros_passivos):
            outros_passivos = 0
        return contas_pagar + outros_passivos

    async def valor_necessidade_capital_giro(self) -> float:
        ativos, passivo = await asyncio.gather(
            self.ativos_circulantes_operacionais(),
            self.passivos_circulantes_operacionais(),
        )
        return ativos - passivo

    async def necessidade_capital_giro_ativo_circulante_menos_passivo_circulante(
        self,
    ) -> float:
        acao = await self.get_balance_sheet()
        if isinstance(acao, pd.DataFrame):
            if "CurrentAssets" in acao.index:
                ativo_circulante = acao.loc["CurrentAssets"][0]
            else:
                ativo_circulante = 0.0
            if "CurrentLiabilities" in acao.index:
                passivo_circulante = acao.loc["CurrentLiabilities"][0]
            else:
                passivo_circulante = 0.0

            necessidade_capital = ativo_circulante - passivo_circulante
            if isinstance(necessidade_capital, pd.Series):
                return float(necessidade_capital.iloc[0])
            return float(necessidade_capital)
        return 0.0
