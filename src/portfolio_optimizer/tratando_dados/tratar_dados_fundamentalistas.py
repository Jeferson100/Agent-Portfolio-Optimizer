from typing import Any, List, Optional

import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

from ..coleta_dados import DadosFundamentalistas


async def tratando_dados_fundamentalistas(
    tic: str,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    colunas_drop: Optional[List[str]] = None,
) -> List[Any]:
    if colunas_drop is None:
        colunas_drop = [
            "acoes_ordinarias",
            "acoes_preferenciais",
            "total",
            "capex_doze_meses",
            "fluxo_caixa_livre_doze_meses",
            "retorno_sobre_capital_tangivel_inicial",
            "retorno_sobre_capital_tangivel_inicial_pre_impostos",
            "retorno_sobre_capital_investido_inicial_pre_impostos",
            "preço_ncav",
            "margem_ebitda",
            "divida_liquida_ebitda",
            "ev_ebitda",
            "ev_receita_líquida",
            "ev_fco",
            "ev_fcf",
            "ev_ativo_total",
            "preço_vpa",
            "preço_capital_giro",
            "preço_fcf",
            "caixa_equivalentes_caixa",
        ]

    dados_fundamentalistas = DadosFundamentalistas(
        tic=tic, data_inicio=data_inicio, data_fim=data_fim
    )

    dados: pd.DataFrame = await dados_fundamentalistas.dados_fundamentalistas_completo()

    dados.drop(columns=colunas_drop, inplace=True, errors="ignore")

    dados["datas"] = dados["datas"].astype(str)

    dados.dropna(axis=1, how="all", inplace=True)

    loader = DataFrameLoader(dados, page_content_column="datas")

    dados_load = loader.load()

    return dados_load
