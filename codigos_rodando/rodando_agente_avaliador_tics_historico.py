from utils import sequencia_datas, run_all_tics, BuildGraphAvaliacaoTics, StateClassification
import json
import logging
import pandas as pd
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
import os
import asyncio
import time
from IPython.display import display, Markdown

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tracer_provider = register(
  project_name="Agente-Criador-Carteira",
  endpoint="https://app.phoenix.arize.com/s/sehnemjeferson/v1/traces",
  auto_instrument=True,
  api_key=os.getenv("PHOENIX_API_KEY")
  
)

LangChainInstrumentor().instrument(tracer_provider=tracer_provider)


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


tics = ["VALE3", "PETR4", "ITUB4", "BBDC4", "ABEV3", 
        "MGLU3", "BBAS3", "GGBR4", "RENT3", "LREN3",
        "PSSA3", "BRAP4", "VIVT3"]

pd_tic = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv"
        )
tics = pd_tic['tic'].unique().tolist()

sequencia_datas = sequencia_datas(start="2020-01-01", end="2025-12-31", freq="QS")

results_dict = {}

for data_inicio, data_fim in sequencia_datas.items():
    display(Markdown(f"## Iniciando o processo para o periodo de {data_inicio} a {data_fim}"))
    try:
        start_time = time.time()
        results_tics = asyncio.run(run_all_tics(
            tics,
            data_inicio=data_inicio,
            data_fim=data_fim
            ))
        
        logger.info(f"Avaliação das acoes foi concluído para {data_inicio} a {data_fim}")    
        
        results_dict[f"{data_inicio}_to_{data_fim}"] = results_tics
        
        
    except Exception as e:
        logger.error(f"Erro ao processar {data_inicio} a {data_fim}: {e}")
        
with open("../data/avaliacao_tics_historico.json", "w") as f:
    json.dump(results_dict, f)
    
logger.info("Processo concluído para todos os períodos.")
    
