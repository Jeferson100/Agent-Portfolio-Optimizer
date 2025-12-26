import asyncio
import time
import logging
import os
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
from portfolio_optimizer import BuildGraphAvaliacaoTics, StateClassification
import json
import datetime
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

graph_tics = BuildGraphAvaliacaoTics()

graph_build = graph_tics.compile()


tics = ["PETR4", "ITUB4", "BBDC4", "ABEV3",
        "BBAS3", "GGBR4", "RENT3", "LREN3",
        "PSSA3", "B3SA3", "BBSE3", "BRAP4", "VIVT3",
        "CSNA3", "BRKM5", "CSUD3", "CGAS3", "CMIG3",
        "WEGE3", "ENBR3", "EGIE3", "ELET3","PRIO3",
        "PSSA3", "MDIA3", "MGLU3", "MRVE3", "NTCO3",
        "IRBR3","FIQE3","FLRY3"]

pd_tic = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv"
        )
tics = pd_tic['tic'].unique().tolist()

data_atual = datetime.datetime.now()

data_atual_str = data_atual.strftime('%Y-%m-%d')

trimestres = pd.date_range(end=data_atual, periods=9, freq='QE')  

data_inicio_str = trimestres[0].strftime('%Y-%m-%d')



async def _invoke_tic(tic: str, data_inicio: str = data_inicio_str, data_fim: str = data_atual_str):
    try:
        start = time.time()
        logger.info(f"🚀 Iniciando {tic}")
        
        result = await graph_build.ainvoke(
            StateClassification({
                "tic": tic,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "avaliacao_analise": "",
                "description_avaliacao_analise": "",
                "interacao": 0,
            })
        )
        
        elapsed = time.time() - start
        logger.info(f"✅ {tic} concluído em {elapsed:.2f}s")
        return result
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar {tic}: {e}")
        return None

logger.info(f"Data de início definida como: {data_inicio_str}")

async def run_all_tics(tics, data_inicio: str = data_inicio_str, data_fim: str = data_atual_str):
    start_total = time.time()
    
    tasks = [_invoke_tic(tic, data_inicio, data_fim) for tic in tics]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)
    
    elapsed_total = time.time() - start_total
    logger.info(f"⏱️  Tempo total: {elapsed_total:.2f}s")
    
    return dict(zip(tics, results_list))


async def main():
    results_tics = await run_all_tics(
        tics
        )
    return results_tics 

if __name__ == "__main__":
    results_tics = asyncio.run(main())
    
    import sys
    sys.path.append('..')
    
    # Criar o diretório se não existir
    os.makedirs("../data", exist_ok=True)

    with open("../data/results_tics.json", "w") as f:
        json.dump(results_tics, f)
    
    

