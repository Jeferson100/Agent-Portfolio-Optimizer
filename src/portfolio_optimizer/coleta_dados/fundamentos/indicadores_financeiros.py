import warnings
from typing import Any, Dict, Union

import numpy as np
import pandas as pd
import yfinance as yf

from .calculo_wacc import CalculoWACC
from .necessidade_capital_giro import NecessidadeCapitalGiro
from .outros_ativos_nao_operecionais import OutrosAtivosNaoOperacionais
from .passivos_menos_divida import PassivoTotalMenosDivida
from .variacao_receita import VariacaoReceita

warnings.filterwarnings("ignore")


class IndicadoresFinanceiros:
    def __init__(
        self,
        ticker: str,
        margem_ebit_mediana: bool = True,
        deflacionar_receita: bool = True,
        percentual_imposto_mediana: bool = True,
        depreciacao_capex_mediana: bool = True,
        capex_receita_mediana: bool = True,
    ):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker=self.ticker)
        self.financials = self.stock.financials
        self.balance_sheet = self.stock.balance_sheet
        self.cashflow = self.stock.cashflow
        self.margem_ebit_mediana = margem_ebit_mediana
        self.deflacionar_receita = deflacionar_receita
        self.percentual_imposto_mediana = percentual_imposto_mediana
        self.depreciacao_capex_mediana = depreciacao_capex_mediana
        self.capex_receita_mediana = capex_receita_mediana

    def ultima_receita(self) -> float:
        receita_ano = self.financials
        if isinstance(receita_ano, pd.DataFrame):
            if "Total Revenue" in receita_ano.index:
                receita_ano = receita_ano.loc["Total Revenue"].iloc[0]
            else:
                receita_ano = 0
            if isinstance(receita_ano, pd.Series):
                return float(receita_ano.iloc[0])
            return float(receita_ano)
        return 0.0

    def variacao_receita_ultimos_anos(self) -> Dict[str, float]:
        variacao_receita = VariacaoReceita(
            ticker=self.ticker, deflacionar_receita=self.deflacionar_receita
        )
        porcentagem_receita = variacao_receita.receita_crescimento_metricas()
        return porcentagem_receita

    def ebit(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        ebit_ultimos_anos = self.financials

        if isinstance(ebit_ultimos_anos, pd.DataFrame):
            if "EBIT" in ebit_ultimos_anos.index:
                return ebit_ultimos_anos.loc["EBIT"]
            elif "Pretax Income" in ebit_ultimos_anos.index:
                return ebit_ultimos_anos.loc["Pretax Income"]
            else:
                # Caso não haja a chave 'EBIT', retornamos uma Series vazia (ou com outro valor padrão)
                return pd.Series(dtype=float)

        elif isinstance(ebit_ultimos_anos, pd.Series):
            return ebit_ultimos_anos

        # Se self.financials não for DataFrame nem Series, retorne uma Series vazia
        return pd.Series(dtype=float)

    def receita(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        receita_ultimos_anos = self.financials

        if isinstance(receita_ultimos_anos, pd.DataFrame):
            if "Total Revenue" in receita_ultimos_anos.index:
                return receita_ultimos_anos.loc["Total Revenue"]
            else:
                # Caso não haja a chave 'Total Revenue', retornamos uma Series vazia (ou com outro valor padrão)
                return pd.Series(dtype=float)

        elif isinstance(receita_ultimos_anos, pd.Series):
            return receita_ultimos_anos

        # Se self.financials não for DataFrame nem Series, retorne uma Series vazia
        return pd.Series(dtype=float)

    def margem_ebit(self) -> float:
        ebit_ultimos_anos = self.ebit()
        receita_ultimos_anos = self.receita()
        try:
            margem_ebit = ebit_ultimos_anos / receita_ultimos_anos

            resultado_margem = (
                margem_ebit.median() if self.margem_ebit_mediana else margem_ebit.mean()
            )

            if isinstance(resultado_margem, (float, int)):
                return round(resultado_margem, 4)  # type: ignore
            elif isinstance(resultado_margem, (pd.DataFrame, pd.Series)):
                return round(resultado_margem.iloc[0], 4)  # type: ignore
            else:
                return 0.05
        except ZeroDivisionError:
            return 0.05

    def imposto(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        imposto_ultimos_anos = self.financials
        if isinstance(imposto_ultimos_anos, pd.DataFrame):
            if "Tax Provision" in imposto_ultimos_anos.index:
                return imposto_ultimos_anos.loc["Tax Provision"]
            else:
                return pd.Series(dtype=float)
        elif isinstance(imposto_ultimos_anos, pd.Series):
            return imposto_ultimos_anos
        return pd.Series(dtype=float)

    def percentual_imposto(self) -> float:
        ebit_ultimos_anos = self.ebit()
        imposto_ultimos_anos = self.imposto()

        tax_ebit = imposto_ultimos_anos / ebit_ultimos_anos

        if isinstance(tax_ebit, pd.DataFrame):
            tax_ebit = tax_ebit.squeeze()

        if isinstance(tax_ebit, pd.Series):
            tax_ebit = tax_ebit[tax_ebit > 0]

            if tax_ebit.empty:
                resultado = 0.30
            else:
                resultado = (
                    tax_ebit.median()
                    if self.percentual_imposto_mediana
                    else tax_ebit.mean()
                )
            return round(float(resultado), 4)
        return 0.30

    def depreciacao_amortizacao(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        depreciacao_amortizacao = self.financials
        if isinstance(depreciacao_amortizacao, pd.DataFrame):
            if "Depreciation And Amortization" in depreciacao_amortizacao.index:
                return depreciacao_amortizacao.loc["Depreciation And Amortization"]
            elif "Reconciled Depreciation" in depreciacao_amortizacao.index:
                return depreciacao_amortizacao.loc["Reconciled Depreciation"]
            else:
                return pd.Series(dtype=float)
        elif isinstance(depreciacao_amortizacao, pd.Series):
            return depreciacao_amortizacao
        return pd.Series(dtype=float)

    def capex(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        capex = self.cashflow
        if isinstance(capex, pd.DataFrame):
            if "Capital Expenditure" in capex.index:
                return capex.loc["Capital Expenditure"]
            else:
                return pd.Series(dtype=float)
        elif isinstance(capex, pd.Series):
            return capex
        return pd.Series(dtype=float)

    def depreciacao_capex(self) -> float:
        depreciacao_amortizacao = self.depreciacao_amortizacao()
        capex = self.capex()

        depre_capex = depreciacao_amortizacao / capex

        if isinstance(depre_capex, pd.DataFrame):
            depre_capex = depre_capex.squeeze()

        resultado_depre = (
            depre_capex.median()
            if self.depreciacao_capex_mediana
            else depre_capex.mean()
        )

        if np.isnan(resultado_depre):
            resultado_depre = 0.1

        if isinstance(resultado_depre, (float, int)):
            return round(abs(resultado_depre), 4)
        elif isinstance(resultado_depre, pd.Series):
            valor = resultado_depre.iloc[0]
            return round(abs(float(valor)), 4)
        elif isinstance(resultado_depre, pd.DataFrame):
            resultado_depre = resultado_depre.squeeze()
            return resultado_depre.mean()
        else:
            return 0.1

    def capex_receita(self) -> float:
        capex = self.capex()
        receita = self.receita()

        capex_recei = capex / receita

        capex_recei_resultado = (
            capex_recei.median() if self.capex_receita_mediana else capex_recei.mean()
        )

        if np.isnan(capex_recei_resultado):
            capex_recei_resultado = 0.1

        if isinstance(capex_recei_resultado, (float, int)):
            return round(abs(capex_recei_resultado), 4)
        elif isinstance(capex_recei_resultado, pd.Series):
            valor = capex_recei_resultado.iloc[0]
            return round(abs(float(valor)), 4)
        elif isinstance(capex_recei_resultado, pd.DataFrame):
            capex_recei_resultado = capex_recei_resultado.squeeze()
            return capex_recei_resultado.mean()
        else:
            return 0.1

    def wacc(self) -> float:
        wac = CalculoWACC(ticker=self.ticker)
        valor_wacc = wac.wacc()
        return valor_wacc

    def quantidade_acoes(self) -> float:
        quantida_acoe = self.stock.quarterly_balance_sheet
        if isinstance(quantida_acoe, pd.DataFrame):
            quantida_acoe = quantida_acoe.squeeze()
        if "Share Issued" in quantida_acoe.index:
            quantida_acoe = quantida_acoe.loc["Share Issued"][0]
        else:
            quantida_acoe = 0.0
        return float(quantida_acoe)

    def divida_total(self) -> float:
        divida_total = self.stock.get_balancesheet(freq="yearly")
        if isinstance(divida_total, pd.DataFrame):
            if "TotalDebt" in divida_total.index:
                divida_total = divida_total.loc["TotalDebt"][0]
            else:
                divida_total = 0.0
            if isinstance(divida_total, pd.Series):
                return float(divida_total.iloc[0])
            return float(divida_total)
        return 0.0

    def caixa_equivalentes_caixa(self) -> float:
        caixa = self.stock.get_balancesheet(freq="yearly")
        if isinstance(caixa, pd.DataFrame):
            if "CashCashEquivalentsAndShortTermInvestments" in caixa.index:
                caixa = caixa.loc["CashCashEquivalentsAndShortTermInvestments"][0]
            else:
                caixa = 0.0
            if isinstance(caixa, pd.Series):
                return float(caixa.iloc[0])
            return float(caixa)
        return 0.0

    def outros_ativos_nao_operacionais(self) -> float:
        outros_nao_ope = OutrosAtivosNaoOperacionais(self.ticker)
        valor_outros = outros_nao_ope.valor_outros_ativos_nao_operacionais()
        return valor_outros

    def passivos_totais_divida(self) -> float:
        passivo_nao_circulante = PassivoTotalMenosDivida(self.ticker)
        valor_passivo_nao_circulante = (
            passivo_nao_circulante.valor_total_passivo_menos_divida()
        )
        return valor_passivo_nao_circulante

    def necessidade_capital_giro(self) -> float:
        necessidade_capital = NecessidadeCapitalGiro(self.ticker)
        valor_necesseidade_capital = necessidade_capital.necessidade_capital_giro_ativo_circulante_menos_passivo_circulante()
        return valor_necesseidade_capital

    def todos_indicadores(self) -> Dict[str, Any]:
        return {
            "margemebit": self.margem_ebit(),
            "ultimareceita": self.ultima_receita(),
            "variacaoreceita": self.variacao_receita_ultimos_anos(),
            "depreciacaocapex": self.depreciacao_capex(),
            "capexreceita": self.capex_receita(),
            "wacc": self.wacc(),
            "quantidadeacoes": self.quantidade_acoes(),
            "dividatotal": self.divida_total(),
            "caixa": self.caixa_equivalentes_caixa(),
            "outrosativos": self.outros_ativos_nao_operacionais(),
            "passivosmenosdivida": self.passivos_totais_divida(),
            "necessidadecapitalgiro": self.necessidade_capital_giro(),
            "percentualimposto": self.percentual_imposto(),
        }
