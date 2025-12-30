import time
import logging
import os
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
from portfolio_optimizer import BuildGraphCriadorCarteira, StateCarteira, transformando_data_frame_para_markdown
import json
from typing import List
import yfinance as yf
import pandas as pd
import time
from IPython.display import display, Markdown
from utils import correlacao, transformando_data_frame_para_markdown, selecionar_tics_bom_excelente
import asyncio

tracer_provider = register(
  project_name="Agente-Criador-Carteira",
  endpoint="https://app.phoenix.arize.com/s/sehnemjeferson/v1/traces",
  auto_instrument=True,
  api_key=os.getenv("PHOENIX_API_KEY")
  
)

LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open("../data/avaliacao_tics_historico.json", "r") as f:
    results_dict = json.load(f)


results_pesos = {}

for datas, dict_tics in results_dict.items():
    display(Markdown(f"## Iniciando o processo para o periodo de {datas}"))
    try:
        start = time.time()
        
        datas_split = datas.split('_to_')
        
        start_data = datas_split[0]
        end_data = datas_split[1]
    
        logger.info(f"Processando período: {datas}")
        
        response = selecionar_tics_bom_excelente(dict_tics)

        dados_markdown = transformando_data_frame_para_markdown(response)
            
        correlacao_tics = correlacao(list(response.keys()), start_data, end_data)
        
        tics = list(response.keys())
        
        gaph_weights = BuildGraphCriadorCarteira()

        graph_weights_build = gaph_weights.compile()
            
        response_pesos = asyncio.run(graph_weights_build.ainvoke(
                StateCarteira({
                "justification" : "",
                "avaliacao_acoes": dados_markdown,
                "correlacao_acoes": correlacao_tics,
                "interacao" : 0,
                "tics" : tics
                })))
            
        results_pesos[f"{datas}"] = response_pesos
            
        logger.info(f"O peso foi calculado para {datas}") 
            
        end_time = time.time()
        execution_time = end_time - start
        logger.info(f"Tempo de execução para {datas}: {execution_time:.2f} segundos")
        
    except Exception as e:
        logger.error(f"Erro ao processar {datas}: {e}")

with open("../data/pesos_carteira_historico.json", "w") as f:
    json.dump(results_pesos, f)