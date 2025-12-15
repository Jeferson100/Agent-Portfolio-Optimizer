import math
import warnings

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")


class NecessidadeCapitalGiro:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.stock = yf.Ticker(ticker=self.ticker)

    def contas_receber(self) -> float:
        contas_receber = self.stock.get_balancesheet(freq="yearly")
        if isinstance(contas_receber, pd.DataFrame):
            if "AccountsReceivable" in contas_receber.index:
                contas_receber = contas_receber.loc["AccountsReceivable"][0]
            else:
                contas_receber = 0
            if isinstance(contas_receber, pd.Series):
                return float(contas_receber.iloc[0])
            return float(contas_receber)
        return 0.0

    def estoque(self) -> float:
        estoque = self.stock.get_balancesheet(freq="yearly")
        if isinstance(estoque, pd.DataFrame):
            if "Inventory" in estoque.index:
                estoque = estoque.loc["Inventory"][0]
            else:
                estoque = 0
            if isinstance(estoque, pd.Series):
                return float(estoque.iloc[0])
            return float(estoque)
        return 0.0

    def outros_ativos_circulantes_operacionais(self) -> float:
        outros_ativos_circulantes_operacionais = self.stock.get_balancesheet(
            freq="yearly"
        )
        if isinstance(outros_ativos_circulantes_operacionais, pd.DataFrame):
            if "OtherCurrentAssets" in outros_ativos_circulantes_operacionais.index:
                outros_ativos_circulantes_operacionais = (
                    outros_ativos_circulantes_operacionais.loc["OtherCurrentAssets"][0]
                )
            else:
                outros_ativos_circulantes_operacionais = 0
            if isinstance(outros_ativos_circulantes_operacionais, pd.Series):
                return float(outros_ativos_circulantes_operacionais.iloc[0])
            return float(outros_ativos_circulantes_operacionais)
        return 0.0

    def outros_passivos_circulantes_operacionais(self) -> float:
        outros_passivo = self.stock.get_balancesheet(freq="yearly")
        if isinstance(outros_passivo, pd.DataFrame):
            if "OtherCurrentLiabilities" in outros_passivo.index:
                outros_passivo = outros_passivo.loc["OtherCurrentLiabilities"][0]
            else:
                outros_passivo = 0
            if isinstance(outros_passivo, pd.Series):
                return float(outros_passivo.iloc[0])
            return float(outros_passivo)
        return 0.0

    def contas_pagar_despesas_acumuladas(self) -> float:
        contas_pagar = self.stock.get_balancesheet(freq="yearly")
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

    def ativos_circulantes_operacionais(self) -> float:
        contas_recebe = self.contas_receber()
        estoques = self.estoque()
        outros_ativos = self.outros_ativos_circulantes_operacionais()
        if math.isnan(contas_recebe):
            contas_recebe = 0
        if math.isnan(estoques):
            estoques = 0
        if math.isnan(outros_ativos):
            outros_ativos = 0
        return contas_recebe + estoques + outros_ativos

    def passivos_circulantes_operacionais(self) -> float:
        contas_pagar = self.contas_pagar_despesas_acumuladas()
        outros_passivos = self.outros_passivos_circulantes_operacionais()
        if math.isnan(contas_pagar):
            contas_pagar = 0
        if math.isnan(outros_passivos):
            outros_passivos = 0
        return contas_pagar + outros_passivos

    def valor_necessidade_capital_giro(self) -> float:
        ativos = self.ativos_circulantes_operacionais()
        passivo = self.passivos_circulantes_operacionais()
        return ativos - passivo

    def necessidade_capital_giro_ativo_circulante_menos_passivo_circulante(
        self,
    ) -> float:
        acao = self.stock.get_balancesheet(freq="yearly")
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
