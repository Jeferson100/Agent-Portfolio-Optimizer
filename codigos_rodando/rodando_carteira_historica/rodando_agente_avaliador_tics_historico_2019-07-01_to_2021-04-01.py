from utils import rodando_tics_sem_sequencia
import json
import logging
import pandas as pd
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
import os
import asyncio
import time
from IPython.display import display, Markdown
import datetime

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


pd_tic = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv"
        )
tics = pd_tic['tic'].unique().tolist()

start_data = "2019-07-01"

end_data = "2021-04-01"
    
results_dict = asyncio.run(rodando_tics_sem_sequencia(start_data, end_data, tics))
        
        
with open(f"../../data/avaliacao_historicos_tics/avaliacao_tics_historico_{start_data}_to_{end_data}.json", "w") as f:
    json.dump(results_dict, f)
    
logger.info("Processo concluído para todos os períodos.")
