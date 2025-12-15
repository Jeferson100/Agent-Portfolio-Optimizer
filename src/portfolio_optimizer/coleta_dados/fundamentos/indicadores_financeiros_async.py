import asyncio
import warnings
from typing import Any, Dict, Union

import numpy as np
import pandas as pd

from ..data_cache import DataCache
from .calculo_wacc_async import CalculoWACCAsync
from .necessidade_capital_giro_async import NecessidadeCapitalGiroAsync
from .outros_ativos_nao_operacionais_async import OutrosAtivosNaoOperacionaisAsync
from .passivos_menos_divida_async import PassivoTotalMenosDividaAsync
from .variacao_receita_async import VariacaoReceitaAsync

warnings.filterwarnings("ignore")

data_cache = DataCache()


class IndicadoresFinanceirosAsync:
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
        self.data_cache = data_cache
        self.margem_ebit_mediana = margem_ebit_mediana
        self.deflacionar_receita = deflacionar_receita
        self.percentual_imposto_mediana = percentual_imposto_mediana
        self.depreciacao_capex_mediana = depreciacao_capex_mediana
        self.capex_receita_mediana = capex_receita_mediana

    async def ultima_receita(self) -> float:
        receita_ano = self.data_cache.get_financials(self.ticker)
        if isinstance(receita_ano, pd.DataFrame):
            if "TotalRevenue" in receita_ano.index:
                receita_ano = receita_ano.loc["TotalRevenue"].iloc[0]
            else:
                receita_ano = 0
            if isinstance(receita_ano, pd.Series):
                return float(receita_ano.iloc[0])
            return float(receita_ano)
        return 0.0

    async def variacao_receita_ultimos_anos(self) -> Dict[str, float]:
        variacao_receita = VariacaoReceitaAsync(
            ticker=self.ticker, deflacionar_receita=self.deflacionar_receita
        )
        porcentagem_receita = await variacao_receita.receita_crescimento_metricas()
        return porcentagem_receita

    async def ebit(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        ebit_ultimos_anos = self.data_cache.get_financials(self.ticker)

        if isinstance(ebit_ultimos_anos, pd.DataFrame):
            if "EBIT" in ebit_ultimos_anos.index:
                return ebit_ultimos_anos.loc["EBIT"]
            elif "PretaxIncome" in ebit_ultimos_anos.index:
                return ebit_ultimos_anos.loc["PretaxIncome"]
            else:
                # Caso não haja a chave 'EBIT', retornamos uma Series vazia (ou com outro valor padrão)
                return pd.Series(dtype=float)

        elif isinstance(ebit_ultimos_anos, pd.Series):
            return ebit_ultimos_anos

        # Se self.financials não for DataFrame nem Series, retorne uma Series vazia
        return pd.Series(dtype=float)

    async def receita(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        receita_ultimos_anos = self.data_cache.get_financials(self.ticker)

        if isinstance(receita_ultimos_anos, pd.DataFrame):
            if "TotalRevenue" in receita_ultimos_anos.index:
                return receita_ultimos_anos.loc["TotalRevenue"]
            else:
                # Caso não haja a chave 'Total Revenue', retornamos uma Series vazia (ou com outro valor padrão)
                return pd.Series(dtype=float)

        elif isinstance(receita_ultimos_anos, pd.Series):
            return receita_ultimos_anos

        # Se self.financials não for DataFrame nem Series, retorne uma Series vazia
        return pd.Series(dtype=float)

    async def margem_ebit(self) -> float:
        ebit_ultimos_anos, receita_ultimos_anos = await asyncio.gather(
            self.ebit(), self.receita()
        )
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

    async def imposto(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        imposto_ultimos_anos = self.data_cache.get_financials(self.ticker)
        if isinstance(imposto_ultimos_anos, pd.DataFrame):
            if "TaxProvision" in imposto_ultimos_anos.index:
                return imposto_ultimos_anos.loc["TaxProvision"]
            else:
                return pd.Series(dtype=float)
        elif isinstance(imposto_ultimos_anos, pd.Series):
            return imposto_ultimos_anos
        return pd.Series(dtype=float)

    async def percentual_imposto(self) -> float:
        ebit_ultimos_anos, imposto_ultimos_anos = await asyncio.gather(
            self.ebit(), self.imposto()
        )

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

    async def depreciacao_amortizacao(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        depreciacao_amortizacao = self.data_cache.get_financials(self.ticker)
        if isinstance(depreciacao_amortizacao, pd.DataFrame):
            if "DepreciationAndAmortization" in depreciacao_amortizacao.index:
                return depreciacao_amortizacao.loc["DepreciationAndAmortization"]
            elif "ReconciledDepreciation" in depreciacao_amortizacao.index:
                return depreciacao_amortizacao.loc["ReconciledDepreciation"]
            else:
                return pd.Series(dtype=float)
        elif isinstance(depreciacao_amortizacao, pd.Series):
            return depreciacao_amortizacao
        return pd.Series(dtype=float)

    async def capex(self) -> Union[pd.Series, pd.DataFrame]:  # type: ignore[type-arg]
        capex = self.data_cache.get_cash_flow(self.ticker)
        if isinstance(capex, pd.DataFrame):
            if "Capital Expenditure" in capex.index:
                return capex.loc["Capital Expenditure"]
            else:
                return pd.Series(dtype=float)
        elif isinstance(capex, pd.Series):
            return capex
        return pd.Series(dtype=float)

    async def depreciacao_capex(self) -> float:
        depreciacao_amortizacao, capex = await asyncio.gather(
            self.depreciacao_amortizacao(), self.capex()
        )

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

    async def capex_receita(self) -> float:
        capex, receita = await asyncio.gather(self.capex(), self.receita())

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

    async def wacc(self) -> float:
        wac = CalculoWACCAsync(ticker=self.ticker)
        valor_wacc = await wac.wacc()
        return valor_wacc

    async def quantidade_acoes(self) -> float:
        quantida_acoe = self.data_cache.get_quarterly_balance_sheet(self.ticker)
        if isinstance(quantida_acoe, pd.DataFrame):
            quantida_acoe = quantida_acoe.squeeze()
        if "Share Issued" in quantida_acoe.index:
            quantida_acoe = quantida_acoe.loc["Share Issued"][0]
        else:
            quantida_acoe = 0.0
        return float(quantida_acoe)

    async def divida_total(self) -> float:
        divida_total = self.data_cache.get_balance_sheet(self.ticker)
        if isinstance(divida_total, pd.DataFrame):
            if "TotalDebt" in divida_total.index:
                divida_total = divida_total.loc["TotalDebt"][0]
            else:
                divida_total = 0.0
            if isinstance(divida_total, pd.Series):
                return float(divida_total.iloc[0])
            return float(divida_total)
        return 0.0

    async def caixa_equivalentes_caixa(self) -> float:
        caixa = self.data_cache.get_balance_sheet(self.ticker)
        if isinstance(caixa, pd.DataFrame):
            if "CashCashEquivalentsAndShortTermInvestments" in caixa.index:
                caixa = caixa.loc["CashCashEquivalentsAndShortTermInvestments"][0]
            else:
                caixa = 0.0
            if isinstance(caixa, pd.Series):
                return float(caixa.iloc[0])
            return float(caixa)
        return 0.0

    async def outros_ativos_nao_operacionais(self) -> float:
        outros_nao_ope = OutrosAtivosNaoOperacionaisAsync(self.ticker)
        valor_outros = await outros_nao_ope.valor_outros_ativos_nao_operacionais()
        return valor_outros

    async def passivos_totais_divida(self) -> float:
        passivo_nao_circulante = PassivoTotalMenosDividaAsync(self.ticker)
        valor_passivo_nao_circulante = (
            await passivo_nao_circulante.valor_total_passivo_menos_divida()
        )
        return valor_passivo_nao_circulante

    async def necessidade_capital_giro(self) -> float:
        necessidade_capital = NecessidadeCapitalGiroAsync(self.ticker)
        valor_necesseidade_capital = await necessidade_capital.necessidade_capital_giro_ativo_circulante_menos_passivo_circulante()
        return valor_necesseidade_capital

    async def todos_indicadores(self) -> Dict[str, Any]:
        (
            margem_ebit,
            ultima_receita,
            variacao_receita,
            depreciacao_capex,
            capex_receita,
            wacc,
            quantidade_acoes,
            divida_total,
            caixa,
            outros_ativos,
            passivos_menos_divida,
            necessidade_capital_giro,
            percentual_imposto,
        ) = await asyncio.gather(  # type: ignore
            self.margem_ebit(),
            self.ultima_receita(),
            self.variacao_receita_ultimos_anos(),
            self.depreciacao_capex(),
            self.capex_receita(),
            self.wacc(),
            self.quantidade_acoes(),
            self.divida_total(),
            self.caixa_equivalentes_caixa(),
            self.outros_ativos_nao_operacionais(),
            self.passivos_totais_divida(),
            self.necessidade_capital_giro(),
            self.percentual_imposto(),
        )

        return {
            "margemebit": margem_ebit,
            "ultimareceita": ultima_receita,
            "variacaoreceita": variacao_receita,
            "depreciacaocapex": depreciacao_capex,
            "capexreceita": capex_receita,
            "wacc": wacc,
            "quantidadeacoes": quantidade_acoes,
            "dividatotal": divida_total,
            "caixa": caixa,
            "outrosativos": outros_ativos,
            "passivosmenosdivida": passivos_menos_divida,
            "necessidadecapitalgiro": necessidade_capital_giro,
            "percentualimposto": percentual_imposto,
        }
