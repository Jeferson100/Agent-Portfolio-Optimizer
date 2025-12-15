import warnings
from datetime import datetime
from typing import Any, Dict, List, Tuple

import pandas as pd

warnings.filterwarnings("ignore")


class ValuationFluxoCaixaDescontado:
    def __init__(
        self,
        receita_ano: float,
        porcenta_crescimento_receita: float,
        margem_ebit: float,
        imposto_porcentagem: float,
        depreciacao_capex: float,
        capex_da_receita: float,
        wacc: float,
        numero_de_acoes: float,
        divida: float,
        disponivel: float,
        ativos_nao_operacionais: float,
        passivos_circulantes: float,
        necessidade_capital_de_giro: float,
        anos_projecao: int = 5,
        taxa_crecimento_perpetuidade: float = 0.014,
        calculo_necessidade_capital_de_giro: bool = True,
    ):
        self.receita_ano = receita_ano
        self.anos_projecao = anos_projecao
        self.porcenta_crescimento_receita = porcenta_crescimento_receita
        self.margem_ebit = margem_ebit
        self.imposto_porcentagem = imposto_porcentagem
        self.depreciacao_capex = depreciacao_capex
        self.capex_da_receita = capex_da_receita
        self.wacc = wacc
        self.numero_de_acoes = numero_de_acoes
        self.divida = divida
        self.disponivel = disponivel
        self.ativos_nao_operacionais = ativos_nao_operacionais
        self.passivos_circulantes = passivos_circulantes
        self.taxa_crecimento_perpetuidade = taxa_crecimento_perpetuidade
        self.necessidade_capital_de_giro = necessidade_capital_de_giro
        self.calculo_necessidade_capital_de_giro = calculo_necessidade_capital_de_giro

    def calcular_periodos(
        self, receita_ano: float, anos: int
    ) -> Tuple[float, float, float, float, float, float, float, float]:
        receita_ano = round(receita_ano * (1 + self.porcenta_crescimento_receita), 2)
        ebit_ano = round(receita_ano * self.margem_ebit, 2)
        imposto_ano = round(ebit_ano * self.imposto_porcentagem, 2)
        capex_ano = round(receita_ano * self.capex_da_receita, 2)
        depreciacao_ano = round(self.depreciacao_capex * capex_ano, 2)
        ebit_ajustado = round(ebit_ano - imposto_ano + depreciacao_ano, 2)
        if self.calculo_necessidade_capital_de_giro:
            fluxo_caixa = ebit_ajustado - capex_ano + self.necessidade_capital_de_giro
        else:
            fluxo_caixa = ebit_ajustado - capex_ano
        valor_presente_fluxo = round(fluxo_caixa / (1 + self.wacc) ** anos, 2)
        return (
            receita_ano,
            ebit_ano,
            imposto_ano,
            capex_ano,
            depreciacao_ano,
            ebit_ajustado,
            fluxo_caixa,
            valor_presente_fluxo,
        )

    def calculo_perpetudidade(
        self, dict_valuation: Dict[str, List[Any]], anos: int
    ) -> Tuple[float, float, float]:
        fluxo_perpetuidade = round(
            (
                dict_valuation["fluxo_caixa"][-1]
                * (1 + self.porcenta_crescimento_receita)
            ),
            2,
        )

        perpetuidade = round(
            fluxo_perpetuidade / (self.wacc - self.taxa_crecimento_perpetuidade), 2
        )

        valor_presente = round(perpetuidade / ((1 + self.wacc) ** anos), 2)

        fluxo_caixa_fluxo_livre = round(
            sum(dict_valuation["valor_presente_fluxo"]) + valor_presente - self.divida,
            2,
        )

        fluxo_caixa_ajustado = round(
            fluxo_caixa_fluxo_livre
            + self.disponivel
            + self.ativos_nao_operacionais
            - self.passivos_circulantes,
            2,
        )

        valor_por_acao = round(fluxo_caixa_ajustado / self.numero_de_acoes, 2)

        return fluxo_caixa_fluxo_livre, fluxo_caixa_ajustado, valor_por_acao

    def calcular_valuation(self) -> tuple[pd.DataFrame, Dict[str, float]]:
        dict_valuation: Dict[str, List[Any]] = {
            "data": [],
            "receita_ano": [],
            "ebit_ano": [],
            "imposto_ano": [],
            "capex_ano": [],
            "depreciacao_ano": [],
            "ebit_ajustado": [],
            "fluxo_caixa": [],
            "valor_presente_fluxo": [],
        }

        receita_ano = self.receita_ano
        now = datetime.now()

        for anos in range(1, self.anos_projecao + 1):
            (
                receita_ano,
                ebit_ano,
                imposto_ano,
                capex_ano,
                depreciacao_ano,
                ebit_ajustado,
                fluxo_caixa,
                valor_presente_fluxo,
            ) = self.calcular_periodos(receita_ano=receita_ano, anos=anos)

            dict_valuation["receita_ano"].append(receita_ano)
            dict_valuation["ebit_ano"].append(ebit_ano)
            dict_valuation["imposto_ano"].append(imposto_ano)
            dict_valuation["capex_ano"].append(capex_ano)
            dict_valuation["depreciacao_ano"].append(depreciacao_ano)
            dict_valuation["ebit_ajustado"].append(ebit_ajustado)
            dict_valuation["fluxo_caixa"].append(fluxo_caixa)
            dict_valuation["valor_presente_fluxo"].append(valor_presente_fluxo)
            dict_valuation["data"].append(now.year + anos - 1)

        fluxo_caixa_fluxo_livre, fluxo_caixa_ajustado, valor_por_acao = (
            self.calculo_perpetudidade(
                dict_valuation=dict_valuation, anos=self.anos_projecao
            )
        )

        dict_perpetuidade = {}
        dict_perpetuidade["fluxo_caixa_fluxo_livre"] = fluxo_caixa_fluxo_livre
        dict_perpetuidade["fluxo_caixa_ajustado"] = fluxo_caixa_ajustado
        dict_perpetuidade["valor_por_acao"] = valor_por_acao

        return pd.DataFrame(dict_valuation), dict_perpetuidade


if __name__ == "__main__":
    from .indicadores_financeiros import IndicadoresFinanceiros

    pd.options.display.float_format = "{:.2f}".format
    ind = IndicadoresFinanceiros(ticker="PETR4.SA")
    indicadores_petr = ind.todos_indicadores()

    valuation = ValuationFluxoCaixaDescontado(
        receita_ano=indicadores_petr["ultimareceita"],
        porcenta_crescimento_receita=(
            indicadores_petr["variacaoreceita"]["mean_deflacionada"]
            if "mean_deflacionada" in indicadores_petr["variacaoreceita"].keys()
            else indicadores_petr["variacaoreceita"]["mean_normal"]
        ),
        margem_ebit=indicadores_petr["margemebit"],
        imposto_porcentagem=indicadores_petr["percentualimposto"],
        depreciacao_capex=indicadores_petr["depreciacaocapex"],
        capex_da_receita=indicadores_petr["capexreceita"],
        wacc=indicadores_petr["wacc"],
        numero_de_acoes=indicadores_petr["quantidadeacoes"],
        divida=indicadores_petr["dividatotal"],
        disponivel=indicadores_petr["caixa"],
        ativos_nao_operacionais=indicadores_petr["outrosativos"],
        passivos_circulantes=indicadores_petr["passivosmenosdivida"],
        necessidade_capital_de_giro=indicadores_petr["necessidadecapitalgiro"],
        anos_projecao=5,
        taxa_crecimento_perpetuidade=0.014,
    )
    print(valuation.calcular_valuation())
