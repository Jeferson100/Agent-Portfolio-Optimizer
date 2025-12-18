"""Portfolio Optimizer - Módulo principal."""

# Re-exporta todos os componentes do módulo agente_investimento
# para permitir imports diretos como: from agente_investimento import 
from .portfolio_optimizer import *  # noqa: F403, F401

__all__ = [
    
    # Coleta de dados
    "DadosFundamentalistas",
    "VerificadorTicks",
    "DadosNoticiasBuscadorYahoo",
    "LinksExtractorHtml",
    "LinksExtractorBS4",
    "LinksExtractorDoclingLoaderAsync",
    "DadosIndicadoresTecnicos",
    "IndicadoresFinanceiros",
    "IndicadoresFinanceirosAsync",
    "CalculoWACC",
    "CalculoWACCAsync",
    "VariacaoReceita",
    "VariacaoReceitaAsync",
    "ValuationModoloGordon",
    "ValuationModoloGordonAsync",
    "OutrosAtivosNaoOperacionais",
    "OutrosAtivosNaoOperacionaisAsync",
    "PassivoTotalMenosDivida",
    "PassivoTotalMenosDividaAsync",
    "NecessidadeCapitalGiro",
    "NecessidadeCapitalGiroAsync",
    "ValuationFluxoCaixaDescontado",
    "ValuationFluxoCaixaDescontadoAsync",
    "DadosNoticiasBuscadorYahooAsync",
    "TratandoDadosIndicadores",
    "TratandoDadosIndicadoresComparacao",
    "TratandoDadosValuation",
    "TratandoDadosValuationComparacao",
    "TratatandoDadosFundamentalistas",
    "LlmRouter",
    "StateCarteira",
    "StateClassification",
    "CarteiraWeights",
    "TickerLevel",
    "SeniorAvaliador",
    "PROMPT_CRIANDO_CARTEIRA",
    "RECOMENDACAO_SENIOR",
    "PROMPT_AVALIADOR_PESOS_CARTEIRA",
    "PROMPT_ANALISE",
    "PROMPT_AVALIADOR",
    "BuildGraphAvaliacaoTics",
    "BuildGraphCriadorCarteira",
    "tratando_resposta_router_llm",
    "normalizar_pesos",
    "transformando_data_frame_para_markdown"
   
]