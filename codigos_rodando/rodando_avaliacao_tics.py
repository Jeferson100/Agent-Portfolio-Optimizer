import asyncio
import time
import logging
import os
from phoenix.otel import register
import phoenix as px
from openinference.instrumentation.langchain import LangChainInstrumentor
from portfolio_optimizer import BuildGraphAvaliacaoTics, StateClassification
import json


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


tics = ["PETR4", "ITUB4", "BBDC4", "ABEV3",] 
tics_2 = ["BBAS3", "GGBR4", "RENT3", "LREN3",
        "PSSA3", "B3SA3", "BBSE3", "BRAP4", "VIVT3",
        "CSNA3", "BRKM5", "CSUD3", "CGAS3", "CMIG3",
        "WEGE3", "ENBR3", "EGIE3", "ELET3","PRIO3",
        "PSSA3", "MDIA3", "MGLU3", "MRVE3", "NTCO3",
        "IRBR3","FIQE3","FLRY3"]


async def _invoke_tic(tic: str, data_inicio: str = "2023-01-01", data_fim: str = "2025-01-01"):
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

async def run_all_tics(tics, data_inicio: str = "2023-01-01", data_fim: str = "2025-01-01"):
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

    with open("../data/results_tics.json", "w") as f:
        json.dump(results_tics, f)
    
    

