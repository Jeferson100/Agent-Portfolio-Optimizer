import asyncio
from typing import Dict, List

import pandas as pd

from ..coleta_dados import (
    IndicadoresFinanceirosAsync,
    ValuationFluxoCaixaDescontadoAsync,
    ValuationModoloGordonAsync,
)
from ..coleta_dados.data_cache import DataCache

data_cache = DataCache()


class TratandoDadosValuationComparacao:
    def __init__(
        self,
        tickers: List[str],
        anos_projecao: int = 5,
        taxa_crescimento_perpetuidade: float = 0.014,
        calculo_necessidade_capital_de_giro: bool = False,
    ) -> None:
        self.tickers = tickers
        self.anos_projecao = anos_projecao
        self.taxa_crescimento_perpetuidade = taxa_crescimento_perpetuidade
        self.calculo_necessidade_capital_de_giro = calculo_necessidade_capital_de_giro
        self.data_cache = data_cache

    async def tratando_ticker(self, ticker: str) -> str:
        if ".SA" in ticker:
            acao = ticker
        else:
            acao = f"{ticker}.SA"
        return acao

    async def preco_atual(self, ticker: str) -> float:
        # acao = yf.Ticker(await self.tratando_ticker(ticker=ticker))
        preco = round(
            self.data_cache.get_history(await self.tratando_ticker(ticker))["Close"][
                -1
            ],
            2,
        )
        return float(preco)

    async def indicadores_financeiros(self, ticker: str) -> Dict[str, float]:
        ind = IndicadoresFinanceirosAsync(
            ticker=await self.tratando_ticker(ticker=ticker)
        )
        indicadores = await ind.todos_indicadores()
        return indicadores

    async def valuation_fluxo_caixa_descontado(
        self, ticker: str
    ) -> tuple[pd.DataFrame, Dict[str, float]]:
        indicadores = await self.indicadores_financeiros(ticker=ticker)
        variacao_receita = indicadores["variacaoreceita"]
        if isinstance(variacao_receita, dict):
            indicadores_variacao_receita = (
                variacao_receita["median_deflacionada"]
                if "median_deflacionada" in variacao_receita.keys()
                else variacao_receita["median_normal"]
            )
        else:
            indicadores_variacao_receita = variacao_receita
        valuation = ValuationFluxoCaixaDescontadoAsync(
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
        fluxo_caixa, valuation_preco = await valuation.calcular_valuation()
        return fluxo_caixa, valuation_preco

    async def valuation_metodo_gordon(self, ticker: str) -> Dict[str, str]:
        valu = ValuationModoloGordonAsync(await self.tratando_ticker(ticker=ticker))
        dicionario = await valu.preco_acao()
        return dicionario

    async def markdow_metodo_gordon(self, ticker: str) -> tuple[str, str]:
        gordon_dados = await self.valuation_metodo_gordon(ticker=ticker)
        markdow_gordon = pd.DataFrame(gordon_dados, index=[0]).to_markdown()
        return markdow_gordon, gordon_dados["valuation_acao"]

    async def markdow_fluxo_caixa_descontado(
        self, ticker: str
    ) -> tuple[str, Dict[str, float]]:
        fluxo_caixa, valuation_preco = await self.valuation_fluxo_caixa_descontado(
            ticker=ticker
        )
        markdow_fluxo = fluxo_caixa.to_markdown()
        return markdow_fluxo, {
            f"Preco do fluxo de caixa para {ticker}": valuation_preco["valor_por_acao"]
        }

    async def markdow_indicadores_financeiros(self, ticker) -> str:
        indicadores = await self.indicadores_financeiros(ticker=ticker)
        markdow_indicadores = pd.DataFrame(indicadores, index=[0]).to_markdown()
        return markdow_indicadores

    async def dados_valuation(self):
        """Executa todas as análises de valuation de forma assíncrona para todos os tickers"""

        gordon_tasks = [self.markdow_metodo_gordon(ticker) for ticker in self.tickers]
        fluxo_tasks = [
            self.markdow_fluxo_caixa_descontado(ticker) for ticker in self.tickers
        ]
        indicadores_tasks = [
            self.markdow_indicadores_financeiros(ticker) for ticker in self.tickers
        ]
        preco_tasks = [self.preco_atual(ticker) for ticker in self.tickers]

        (
            gordon_results,
            fluxo_results,
            indicadores_results,
            preco_results,
        ) = await asyncio.gather(
            asyncio.gather(*gordon_tasks),
            asyncio.gather(*fluxo_tasks),
            asyncio.gather(*indicadores_tasks),
            asyncio.gather(*preco_tasks),
        )

        tasks = {}
        for i, ticker in enumerate(self.tickers):
            tasks[ticker] = [
                gordon_results[i],
                fluxo_results[i],
                indicadores_results[i],
                preco_results[i],
            ]

        return tasks
