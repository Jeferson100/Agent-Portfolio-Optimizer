import asyncio
import time
import logging
import os
from phoenix.otel import register
import phoenix as px
from openinference.instrumentation.langchain import LangChainInstrumentor
from portfolio_optimizer import BuildGraphCriadorCarteira, StateCarteira
import json
from typing import List
import yfinance as yf
import pandas as pd



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tracer_provider = register(
  project_name="Agente-Criador-Carteira",
  endpoint="https://app.phoenix.arize.com/s/sehnemjeferson/v1/traces",
  auto_instrument=True,
  api_key=os.getenv("PHOENIX_API_KEY")
  
)

LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

def transformando_data_frame_para_markdown(results):
    try:
        results_pd = pd.DataFrame.from_dict(results).T
    except Exception as e:
        results_pd = pd.DataFrame.from_dict(results, orient="index").T
    dados_markdown = results_pd.loc[:, ["classification", "analysis"]].reset_index().rename(columns={"index": "tic"}).to_markdown()
    return dados_markdown

def correlacao(tics:List[str]):
        tics_yf = [tic + ".SA" for tic in tics]

        df = yf.download(tics_yf, start="2023-01-01", end="2025-01-01", interval="1mo")["Close"]
        returns = df.pct_change()[4:]
        # Calcula a matriz de correlação
        correlacao = returns.corr()

        return correlacao.to_markdown()

logger.info("Iniciando avaliação das ações. Carregando dados...")

with open("../data/results_tics.json", "r") as f:
    response = json.load(f)

logger.info("Dados carregados com sucesso. Transformando em DataFrame...")

response_markdown = transformando_data_frame_para_markdown(response)

logger.info("DataFrame transformado com sucesso. Calculando correlação...")

corr_tics = correlacao(list(response.keys()))

logger.info("Correlação calculada com sucesso. Criando carteira...")

gaph_weights = BuildGraphCriadorCarteira()

graph_weights_build = gaph_weights.compile()

tics = list(response.keys())

async def run_create_carteira():
    response_pesos = await graph_weights_build.ainvoke(
            StateCarteira({
            "justification" : "",
            "avaliacao_acoes": response_markdown ,
            "correlacao_acoes": corr_tics,
            "interacao" : 0,
            "tics": tics
            }))
    return response_pesos

if __name__ == "__main__":
    resultado_carteira = asyncio.run(run_create_carteira())
    
    logger.info(f"Resultado da Carteira: {resultado_carteira}")
    
    with open("../data/carteira_resultado.json", "w") as f:
        json.dump(resultado_carteira, f)
