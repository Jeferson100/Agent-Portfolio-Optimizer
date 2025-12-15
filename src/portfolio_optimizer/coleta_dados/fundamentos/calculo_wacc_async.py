import asyncio
import warnings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pandas as pd

from ..data_cache import DataCache

warnings.filterwarnings("ignore")

cache = DataCache()


class CalculoWACCAsync:
    def __init__(
        self,
        ticker: str,
        start_date_retorno: str = "2004-01-01",
        end_date_retorno: str = datetime.today().strftime("%Y-%m-%d"),
    ):
        self.ticker = self.tratando_ticker(ticker)
        self.start_date_retorno = start_date_retorno
        self.end_date_retorno = end_date_retorno
        self.cache = cache  # Usa o cache global

    def tratando_ticker(self, ticker: str) -> str:
        if ".SA" in ticker:
            acao = ticker
        else:
            acao = f"{ticker}.SA"
        return acao

    async def initialize(self):
        """Pré-carrega todos os dados necessários para evitar múltiplas chamadas."""
        with ThreadPoolExecutor(max_workers=3) as executor:
            info_future = executor.submit(self.cache.get_info, self.ticker)
            dividends_future = executor.submit(self.cache.get_dividends, self.ticker)
            history_future = executor.submit(self.cache.get_history, self.ticker)

            # Aguardar a conclusão
            self.info = (  # pylint: disable=attribute-defined-outside-init # type: ignore
                info_future.result()  # pylint: disable=attribute-defined-outside-init # type: ignore
            )  # pylint: disable=attribute-defined-outside-init
            self.dividends = (  # pylint: disable=attribute-defined-outside-init # type: ignore
                dividends_future.result()  # pylint: disable=attribute-defined-outside-init
            )  # pylint: disable=attribute-defined-outside-init
            self.history = (  # pylint: disable=attribute-defined-outside-init # type: ignore
                history_future.result()  # pylint: disable=attribute-defined-outside-init
            )  # pylint: disable=attribute-defined-outside-init

    async def juros_livre(self) -> float:
        try:
            cach_juros = self.cache.get_ipea_data("BMF12_SWAPDI36012")
            df_juros = pd.DataFrame(cach_juros)
            juros = (
                df_juros.rename(columns={"VALUE ((% a.a.))": "swaps"})[["swaps"]]
                .div(100)
                .iloc[-1]
                .swaps
            )
            if juros is None:
                raise ValueError("Erro: Não foi possível obter os juros livres.")
            return float(juros)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Erro ao obter juros livres: {e}")
            return 0.1  # Taxa padrão em caso de erro

    async def retorno_mercado(self) -> float:
        try:
            ibov = self.cache.get_dowload("^BVSP")
            ibov = pd.DataFrame(ibov)

            if ibov is None or ibov.empty:
                raise ValueError("Erro: Nenhum dado foi baixado para o IBOVESPA.")

            if "Close" not in ibov.columns:
                raise ValueError("Erro: A coluna 'Close' não está presente nos dados.")

            porcentagem = ibov.pct_change()["Close"]
            porcentagem.dropna(axis=0, inplace=True)
            compounded_growth = (1 + porcentagem).prod()
            n_periods = porcentagem.shape[0]
            retorno_medio = compounded_growth ** (252 / n_periods) - 1

            return float(retorno_medio["^BVSP"])
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Erro ao calcular retorno do mercado: {e}")
            return 0.15  # Retorno padrão em caso de erro

    async def valor_mercado(self):
        """Obtém o valor de mercado da empresa."""
        # Usa o cache em vez de fazer nova chamada
        info = self.cache.get_info(self.ticker)
        market_cap = info.get("marketCap", 0)
        if market_cap is None:
            raise ValueError("Erro: Não foi possível obter os valores de mercado.")
        return float(market_cap)

    async def valor_total_empresa(self) -> float:
        info = self.cache.get_info(self.ticker)
        enterprise_value = info.get("enterpriseValue", 0)
        if enterprise_value is None:
            raise ValueError("Erro: Não foi possível obter o valor total da empresa.")
        return float(enterprise_value)

    async def calculo_divida(self) -> float:
        valor_mercado, valor_total = await asyncio.gather(
            self.valor_mercado(), self.valor_total_empresa()
        )
        debt = valor_total - valor_mercado if valor_total and valor_mercado else 0
        return float(debt)

    async def beta_empresa(self) -> float:
        info = self.cache.get_info(self.ticker)
        beta = info.get("beta", 1)
        if beta is None:
            raise ValueError("Erro: Não foi possível obter o beta da empresa.")
        return float(beta)

    async def custo_patrimonio(self) -> float:
        juros, beta, retorno = await asyncio.gather(
            self.juros_livre(), self.beta_empresa(), self.retorno_mercado()
        )
        cost_of_equity = juros + beta * retorno
        if cost_of_equity is None:
            raise ValueError("Erro: Não foi possível obter o custo do patrimônio.")
        return float(cost_of_equity)

    async def despesas_juros(self) -> float:
        financials = self.cache.get_financials(self.ticker)

        if not isinstance(financials, pd.DataFrame):
            df_financials = pd.DataFrame.from_dict(financials)
        else:
            df_financials = financials

        if df_financials.empty:
            raise ValueError("Erro: Nenhum dado financeiro encontrado.")

        if "InterestExpense" not in df_financials.index:
            raise ValueError(
                "Erro: A coluna 'InterestExpense' não está presente nos dados financeiros."
            )

        return float(df_financials.loc["InterestExpense"].values[0])

    async def total_divida(self) -> float:
        info = self.cache.get_info(self.ticker)
        total_debt = info.get("totalDebt", 0)
        if total_debt is None:
            raise ValueError("Erro: Não foi possível obter o total da divida.")
        return float(total_debt)

    async def custo_divida(self) -> float:
        despesas, total_divida, juros = await asyncio.gather(
            self.despesas_juros(), self.total_divida(), self.juros_livre()
        )

        cost_of_debt = (despesas / total_divida) if total_divida else juros
        return cost_of_debt

    async def custo_imposto(self) -> float:
        ticker = self.cache.get_ticker(self.ticker)
        tax_provision = ticker.financials.loc["Tax Provision"].values[0]
        pretax_income = ticker.financials.loc["Pretax Income"].values[0]
        tax_rate = tax_provision / pretax_income if pretax_income else 0.30
        return tax_rate

    async def wacc(self) -> float:
        try:
            results = await asyncio.gather(
                self.valor_mercado(),
                self.calculo_divida(),
                self.custo_patrimonio(),
                self.total_divida(),
                self.custo_divida(),
                self.custo_imposto(),
                self.juros_livre(),
            )

            # Desempacota os resultados
            (
                valor_mercado,
                calculo_divida,
                custo_patrimonio,
                total_divida,
                custo_divida,
                custo_imposto,
                juros,
            ) = results

            V = (
                (valor_mercado + calculo_divida)
                if valor_mercado and calculo_divida
                else 1
            )

            wacc = (valor_mercado / V * custo_patrimonio) + (
                total_divida / V * custo_divida * (1 - custo_imposto)
            )

            if wacc <= 0:
                wacc = juros
        except (  # pylint: disable=broad-exception-caught
            Exception,  # pylint: disable=broad-exception-caught
            ValueError,  # pylint: disable=broad-exception-caught
            TypeError,  # pylint: disable=broad-exception-caught
            AttributeError,
        ) as e:  # pylint: disable=broad-exception-caught
            print(f"Erro ao calcular WACC: {e}")
            wacc = await self.juros_livre()

        return round(wacc, 3)
