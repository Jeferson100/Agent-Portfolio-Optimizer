import warnings
from datetime import datetime

import ipeadatapy as ip
import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")


class CalculoWACC:
    def __init__(
        self,
        ticker: str,
        start_date_retorno: str = "2004-01-01",
        end_date_retorno: str = datetime.today().strftime("%Y-%m-%d"),
    ):
        self.ticker = self.tratando_ticker(ticker)
        self.empresa = yf.Ticker(self.ticker)
        self.start_date_retorno = start_date_retorno
        self.end_date_retorno = end_date_retorno

    def tratando_ticker(self, ticker: str) -> str:
        if ".SA" in ticker:
            acao = ticker
        else:
            acao = f"{ticker}.SA"
        return acao

    def juros_livre(self) -> float:
        juros = (
            ip.timeseries("BMF12_SWAPDI36012")  # type: ignore
            .rename(columns={"VALUE ((% a.a.))": "swaps"})[["swaps"]]
            .div(100)
            .iloc[-1]
            .swaps
        )
        if juros is None:
            raise ValueError("Erro: Não foi possível obter os juros livres.")
        return float(juros)

    def retorno_mercado(self) -> float:
        ibov = yf.download(
            "^BVSP", start=self.start_date_retorno, end=self.end_date_retorno
        )

        if ibov is None or ibov.empty:
            raise ValueError("Erro: Nenhum dado foi baixado para o IBOVESPA.")

        # Garantir que a coluna 'Close' existe
        if "Close" not in ibov.columns:
            raise ValueError("Erro: A coluna 'Close' não está presente nos dados.")

        porcentagem = ibov.pct_change()["Close"]

        porcentagem.dropna(axis=0, inplace=True)

        compounded_growth = (1 + porcentagem).prod()

        n_periods = porcentagem.shape[0]

        retorno_medio = compounded_growth ** (252 / n_periods) - 1

        return float(retorno_medio["^BVSP"])

    def valor_mercado(self) -> float:
        market_cap = self.empresa.info.get("marketCap", 0)
        if market_cap is None:
            raise ValueError("Erro: Não foi possível obter os valores de mercado.")

        # Certifique-se de que juros é um float
        return float(market_cap)

    def valor_total_empresa(self) -> float:
        enterprise_value = self.empresa.info.get("enterpriseValue", 0)
        if enterprise_value is None:
            raise ValueError("Erro: Não foi possível obter o valor total da empresa.")
        return float(enterprise_value)

    def calculo_divida(self) -> float:
        debt = (
            self.valor_total_empresa() - self.valor_mercado()
            if self.valor_total_empresa() and self.valor_mercado()
            else 0
        )
        if debt is None:
            raise ValueError("Erro: Não foi possível obter o valor total da empresa.")
        return float(debt)

    def beta_empresa(self) -> float:
        beta = self.empresa.info.get("beta", 1)
        if beta is None:
            raise ValueError("Erro: Não foi possível obter o beta da empresa.")
        return float(beta)

    def custo_patrimonio(self) -> float:
        cost_of_equity = (
            self.juros_livre() + self.beta_empresa() * self.retorno_mercado()
        )
        if cost_of_equity is None:
            raise ValueError("Erro: Não foi possível obter o custo do patrimônio.")
        return float(cost_of_equity)

    def despesas_juros(self) -> float:
        financials = self.empresa.get_financials()

        # Se não for DataFrame, converter
        if not isinstance(financials, pd.DataFrame):
            df_financials = pd.DataFrame.from_dict(financials)
        else:
            df_financials = financials

        if df_financials.empty:
            raise ValueError("Erro: Nenhum dado financeiro encontrado.")

        # Verifique se a coluna 'Interest Expense' existe
        if "InterestExpense" not in df_financials.index:
            raise ValueError(
                "Erro: A coluna 'InterestExpense' não está presente nos dados financeiros."
            )

        return float(df_financials.loc["InterestExpense"].values[0])

    def total_divida(self) -> float:
        total_debt = self.empresa.info.get("totalDebt", 0)
        if total_debt is None:
            raise ValueError("Erro: Não foi possível obter o total da divida.")
        return float(total_debt)

    def custo_divida(self) -> float:
        cost_of_debt = (
            (self.despesas_juros() / self.total_divida())
            if self.total_divida()
            else self.juros_livre()
        )
        return cost_of_debt

    def custo_imposto(self) -> float:
        tax_provision = self.empresa.financials.loc["Tax Provision"].values[0]
        pretax_income = self.empresa.financials.loc["Pretax Income"].values[0]
        tax_rate = tax_provision / pretax_income if pretax_income else 0.30
        return tax_rate

    def wacc(self) -> float:
        try:
            V = (
                self.valor_mercado() + self.calculo_divida()
                if self.valor_mercado() and self.calculo_divida()
                else 1
            )  # Evita divisão por zero

            wacc = (self.valor_mercado() / V * self.custo_patrimonio()) + (
                self.total_divida()
                / V
                * self.custo_divida()
                * (1 - self.custo_imposto())
            )

            if wacc <= 0:
                wacc = self.juros_livre()
        except (  # pylint: disable=broad-exception-caught
            Exception,
            ValueError,
            TypeError,
            AttributeError,
        ) as e:  # pylint: disable=broad-exception-caught
            print(f"Erro ao calcular o WACC: {e}")
            wacc = self.juros_livre()

        return round(wacc, 3)
