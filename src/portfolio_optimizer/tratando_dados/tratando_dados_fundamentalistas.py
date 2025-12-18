import asyncio
from typing import List, Optional

import pandas as pd

from ..coleta_dados import DadosFundamentalistas

import logging

logger = logging.getLogger(__name__)

class TratatandoDadosFundamentalistas:
    """
    Classe para tratamento e processamento de dados fundamentalistas de ações.
    
    Esta classe gerencia a coleta, seleção, preenchimento de datas faltantes e 
    deslocamento temporal de dados fundamentalistas de empresas listadas em bolsa.
    
    Attributes:
        tics (str): Código do ticker da ação (ex: 'PETR4', 'VALE3')
        data_inicio (Optional[str]): Data inicial para coleta no formato 'YYYY-MM-DD'
        data_fim (Optional[str]): Data final para coleta no formato 'YYYY-MM-DD'
        colunas_drop (Optional[List[str]]): Lista de colunas a serem removidas (não utilizado)
        periodos_deslocados (int): Número de períodos para deslocar os dados (padrão: 1)
    
    Example:
        >>> tratador = TratatandoDadosFundamentalistas(
        ...     tics='PETR4',
        ...     data_inicio='2020-01-01',
        ...     data_fim='2024-12-31',
        ...     periodos_deslocados=1
        ... )
        >>> df = await tratador.coleta_dados_fundamentalistas()
    """
    def __init__(
        self,
        tics: str,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        colunas_drop: Optional[List[str]] = None,
        periodos_deslocados: int = 1
    ) -> None:
        """
        Inicializa o tratador de dados fundamentalistas.
        
        Args:
            tics: Código do ticker da ação
            data_inicio: Data inicial no formato 'YYYY-MM-DD'. Se None, usa últimos 4 trimestres
            data_fim: Data final no formato 'YYYY-MM-DD'
            colunas_drop: Lista de colunas a remover (funcionalidade não implementada)
            periodos_deslocados: Número de períodos trimestrais para deslocar os dados
        """
        self.tics = tics
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.colunas_drop = colunas_drop
        self.periodos_deslocados = periodos_deslocados

    async def dados_fundamentalistas(self) -> pd.DataFrame | None:
        """
        Coleta dados fundamentalistas da ação especificada.
        
        Se data_inicio não for fornecida, retorna apenas os últimos 4 trimestres.
        Utiliza a classe DadosFundamentalistas para buscar os dados.
        
        Returns:
            DataFrame com dados fundamentalistas completos ou None em caso de erro
            
        Raises:
            Exception: Loga erro se houver falha na coleta dos dados
            
        Note:
            Se data_inicio não for especificada, automaticamente seleciona
            dados a partir do 4º trimestre mais antigo disponível
        """
        try:
            df = DadosFundamentalistas(
                    tic=self.tics, data_inicio=self.data_inicio, data_fim=self.data_fim
                )
            df_dados = await df.dados_fundamentalistas_completo()
            if self.data_inicio:
                return df_dados
            data_inicio = df_dados["datas"].iloc[-4].strftime("%Y-%m-%d")
            df_data_inicio = df_dados.loc[df_dados.datas >= data_inicio]
            return df_data_inicio
        except Exception as e:
            logger.error(f"Erro ao coletar dados fundamentalistas para {self.tics}: {e}")
            
    
    async def completando_datas_faltantes(self) -> pd.DataFrame:
        """
        Completa datas faltantes no DataFrame com frequência trimestral.
        
        Preenche lacunas temporais entre a última data disponível e data_fim,
        criando registros trimestrais e propagando valores anteriores (forward fill).
        
        Returns:
            DataFrame com datas completas em frequência trimestral
            
        Raises:
            ValueError: Se DataFrame estiver vazio ou sem coluna 'datas'
            
        Note:
            - Utiliza frequência 'QE' (Quarter End) para datas trimestrais
            - Aplica forward fill para preencher valores das novas datas
            - Se data_fim <= última data disponível, retorna DataFrame original
        """
        
        df = await self.selecionando_colunas()
        
        if not isinstance(df, pd.DataFrame):
            return pd.DataFrame()
        
        if df.empty or 'datas' not in df.columns:
            raise ValueError("DataFrame vazio ou sem coluna 'datas'")
        
        df = df.copy()
        
        df['datas'] = pd.to_datetime(df['datas'])
        
        ultima_data = df['datas'].max()
        
        data_fim_dt = pd.to_datetime(self.data_fim)  #type:ignore
        
        if data_fim_dt <= ultima_data:
            return df
        
        proxima_data = ultima_data + pd.DateOffset(months=3)
        dates_faltantes = pd.date_range(
            start=proxima_data,
            end=data_fim_dt,
            freq='QE'  
        )
        
        df_faltantes = pd.DataFrame({'datas': dates_faltantes})
        
        resultado = pd.concat([df, df_faltantes], ignore_index=True).sort_values('datas')
        
        resultado = resultado.ffill()
        
        return resultado
            
    async def selecionando_colunas(self) -> pd.DataFrame | None:
        """
        Seleciona colunas específicas dos dados fundamentalistas.
        
        Filtra apenas as colunas de interesse para análise fundamentalista,
        incluindo indicadores financeiros, de valuation e fluxo de caixa.
        
        Returns:
            DataFrame com colunas selecionadas ou None se dados não disponíveis
            
        Note:
            Colunas selecionadas:
            - receita_liquida: Receita líquida da empresa
            - ebitda: EBITDA (lucro antes de juros, impostos, depreciação e amortização)
            - lucro_por_acao: LPA (Lucro Por Ação)
            - datas: Data de referência dos dados
            - tic: Ticker da ação
            - alavancagem_financeira: Índice de alavancagem
            - margem_liquida: Margem líquida de lucro
            - preço_lucro: Índice P/L (Preço/Lucro)
            - preço_vpa: Índice P/VPA (Preço/Valor Patrimonial por Ação)
            - fluxo_caixa_operacional: FCO (Fluxo de Caixa Operacional)
            - divida_liquida_ebitda: Relação Dívida Líquida/EBITDA
            - aumento_reducao_caixa_equivalentes: Variação de caixa
        """
        
        colunas_selecionadas = ['receita_liquida',
        'ebitda',
        'lucro_por_acao','datas', 'tic',
        'alavancagem_financeira',
        'margem_liquida','preço_lucro', 'preço_vpa',
        'fluxo_caixa_operacional',
        'divida_liquida_ebitda',
        'aumento_reducao_caixa_equivalentes']
        
        df = await self.dados_fundamentalistas()
        
        if df is None or df.empty:
            return None  

        df_selecionado = df.loc[:, colunas_selecionadas]

        df_selecionado["datas"] = df_selecionado["datas"].astype(str)

        return df_selecionado
    
    
    async def deslocar_dados(self) -> pd.DataFrame:
        """
        Desloca temporalmente os dados fundamentalistas.
        
        Aplica shift nos dados para criar lag temporal, útil para evitar look-ahead bias
        em modelos preditivos. Por exemplo, com periodos_deslocados=1, os dados do
        trimestre atual ficam associados à data do próximo trimestre.
        
        Returns:
            DataFrame com dados deslocados temporalmente
            
        Note:
            - A coluna 'datas' não é deslocada, mantendo referência temporal
            - Todas as outras colunas são deslocadas conforme periodos_deslocados
            - Útil para garantir que previsões usem apenas dados disponíveis no passado
            
        Example:
            Com periodos_deslocados=1:
            Data original: 2024-Q1 -> Dados de 2023-Q4
            Data original: 2024-Q2 -> Dados de 2024-Q1
        """
        
        dados = await self.completando_datas_faltantes()
        
        if dados is None:
            return pd.DataFrame()
        
        dados_deslocados = dados.copy()
        
        colunas_para_deslocar = dados.columns.drop('datas')
        
        dados_deslocados[colunas_para_deslocar] = dados[colunas_para_deslocar].shift(self.periodos_deslocados)
        
        return dados_deslocados
    
    async def coleta_dados_fundamentalistas(self) -> pd.DataFrame:
        """
        Método principal para coletar dados fundamentalistas processados.
        
        Executa todo o pipeline de tratamento:
        1. Coleta dados brutos
        2. Seleciona colunas relevantes
        3. Completa datas faltantes
        4. Desloca dados temporalmente
        
        Returns:
            DataFrame final com dados fundamentalistas prontos para uso
            
        Example:
            >>> tratador = TratatandoDadosFundamentalistas(
            ...     tics='PETR4',
            ...     data_inicio='2020-01-01',
            ...     data_fim='2024-12-31',
            ...     periodos_deslocados=1
            ... )
            >>> df_final = await tratador.coleta_dados_fundamentalistas()
        """
        dados = await self.deslocar_dados()
        return dados[1:]
