import asyncio
from typing import List, Optional

import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

from ..coleta_dados import DadosFundamentalistas

import logging

logger = logging.getLogger(__name__)

class TratatandoDadosFundamentalistasComparacao:
    def __init__(
        self,
        tics: List[str],
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        colunas_drop: Optional[List[str]] = None,
    ) -> None:
        self.tics = tics
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.colunas_drop = colunas_drop

    async def dados_fundamentalistas(self, tic: str) -> pd.DataFrame | None:
        try:
            df = DadosFundamentalistas(
                    tic=tic, data_inicio=self.data_inicio, data_fim=self.data_fim
                )
            df_dados = await df.dados_fundamentalistas_completo()
            if self.data_inicio:
                return df_dados
            data_inicio = df_dados["datas"].iloc[-4].strftime("%Y-%m-%d")
            df_data_inicio = df_dados.loc[df_dados.datas >= data_inicio]
            return df_data_inicio
        except Exception as e:
            logger.error(f"Erro ao coletar dados fundamentalistas para {tic}: {e}")
            
    async def selecionando_colunas(self, tic: str) -> pd.DataFrame:
        
        colunas_selecionadas = ['receita_liquida',
        'ebitda',
        'lucro_por_acao','datas', 'tic',
        'alavancagem_financeira',
        'margem_liquida','preço_lucro', 'preço_vpa',
        'fluxo_caixa_operacional',
        'divida_liquida_ebitda',
        'aumento_reducao_caixa_equivalentes']
        
        df = await self.dados_fundamentalistas(tic=tic)
        
        if df is None or df.empty:
            return None  

        df_selecionado = df.loc[:, colunas_selecionadas]

        df_selecionado["datas"] = df_selecionado["datas"].astype(str)

        return df_selecionado
        

    async def transformer_loader(self, tic: str):
        dados_drop = await self.selecionando_colunas(tic=tic)
        
        if dados_drop is None or dados_drop.empty:
            print(f"Pulando ticker sem dados: {tic}")
            return None

        loader = DataFrameLoader(dados_drop, page_content_column="datas")

        dados_load = loader.load()

        return dados_load

    async def coletando_dados_tickers(self):
        resutado_ticks = await asyncio.gather(
            *[self.selecionando_colunas(tic=tic) for tic in self.tics]
        )

        return resutado_ticks
