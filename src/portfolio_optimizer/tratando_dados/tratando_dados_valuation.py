from typing import Dict

import pandas as pd
import yfinance as yf

from ..coleta_dados.fundamentos.indicadores_financeiros import IndicadoresFinanceiros
from ..coleta_dados.fundamentos.valuation_fluxo_caixa_descontado import (
    ValuationFluxoCaixaDescontado,
)
from ..coleta_dados.fundamentos.valuation_metodo_gordon import ValuationModoloGordon


class TratandoDadosValuation:
    def __init__(
        self,
        ticker: str,
        anos_projecao: int = 5,
        taxa_crescimento_perpetuidade: float = 0.014,
        calculo_necessidade_capital_de_giro: bool = False,
    ) -> None:
        self.ticker = ticker
        self.anos_projecao = anos_projecao
        self.taxa_crescimento_perpetuidade = taxa_crescimento_perpetuidade
        self.calculo_necessidade_capital_de_giro = calculo_necessidade_capital_de_giro

    def tratando_ticker(self) -> str:
        if ".SA" in self.ticker:
            acao = self.ticker
        else:
            acao = f"{self.ticker}.SA"
        return acao

    def preco_atual(self) -> float:
        acao = yf.Ticker(self.tratando_ticker())
        preco = round(acao.history(period="1Y", interval="1d")["Close"][-1], 2)
        return float(preco)

    def indicadores_financeiros(self) -> Dict[str, float]:
        ind = IndicadoresFinanceiros(ticker=self.tratando_ticker())
        indicadores = ind.todos_indicadores()
        return indicadores

    def valuation_fluxo_caixa_descontado(self) -> tuple[pd.DataFrame, Dict[str, float]]:
        indicadores = self.indicadores_financeiros()
        variacao_receita = indicadores["variacaoreceita"]
        if isinstance(variacao_receita, dict):
            indicadores_variacao_receita = (
                variacao_receita["median_deflacionada"]
                if "median_deflacionada" in variacao_receita.keys()
                else variacao_receita["median_normal"]
            )
        else:
            indicadores_variacao_receita = variacao_receita
        valuation = ValuationFluxoCaixaDescontado(
            receita_ano=indicadores["ultimareceita"],
            porcenta_crescimento_receita=indicadores_variacao_receita,
            margem_ebit=indicadores["margemebit"],
            imposto_porcentagem=indicadores["percentualimposto"],
            depreciacao_capex=indicadores["depreciacaocapex"],
            capex_da_receita=indicadores["capexreceita"],
            wacc=indicadores["wacc"],
            numero_de_acoes=indicadores["quantidadeacoes"],
            divida=indicadores["dividatotal"],
            disponivel=indicadores["caixa"],
            ativos_nao_operacionais=indicadores["outrosativos"],
            passivos_circulantes=indicadores["passivosmenosdivida"],
            necessidade_capital_de_giro=indicadores["necessidadecapitalgiro"],
            anos_projecao=self.anos_projecao,
            taxa_crecimento_perpetuidade=self.taxa_crescimento_perpetuidade,
            calculo_necessidade_capital_de_giro=self.calculo_necessidade_capital_de_giro,
        )
        fluxo_caixa, valuation_preco = valuation.calcular_valuation()
        return fluxo_caixa, valuation_preco

    def valuation_metodo_gordon(self) -> Dict[str, str]:
        valu = ValuationModoloGordon(self.tratando_ticker())
        dicionario = valu.preco_acao()
        return dicionario

    def markdow_metodo_gordon(self) -> tuple[str, str]:
        gordon_dados = self.valuation_metodo_gordon()
        markdow_gordon = pd.DataFrame(gordon_dados, index=[0]).to_markdown()
        return markdow_gordon, gordon_dados["valuation_acao"]

    def markdow_fluxo_caixa_descontado(self) -> tuple[str, float]:
        fluxo_caixa, valuation_preco = self.valuation_fluxo_caixa_descontado()
        markdow_fluxo = fluxo_caixa.to_markdown()
        return markdow_fluxo, valuation_preco["valor_por_acao"]

    def markdow_indicadores_financeiros(self) -> str:
        indicadores = self.indicadores_financeiros()
        markdow_indicadores = pd.DataFrame(indicadores, index=[0]).to_markdown()
        return markdow_indicadores

    def dados_valuation(self) -> tuple[str, str, str, str]:
        markdow_gordon, preco_gordon = self.markdow_metodo_gordon()
        markdow_fluxo, preco_fluxo = self.markdow_fluxo_caixa_descontado()
        markdow_indicadores = self.markdow_indicadores_financeiros()
        preco_atual = self.preco_atual()
        dict_preco = {
            "preco_gordon": str(preco_gordon),
            "preco_fluxo": str(preco_fluxo),
            "preco_atual": str(preco_atual),
        }

        df_preco = pd.DataFrame(dict_preco, index=[0])

        markdow_preco: str = df_preco.to_markdown()

        return markdow_gordon, markdow_fluxo, markdow_preco, markdow_indicadores
