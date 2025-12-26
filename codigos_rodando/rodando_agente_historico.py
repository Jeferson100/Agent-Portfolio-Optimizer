from utils import sequencia_datas,run_all_tics, transformando_data_frame_para_markdown, correlacao, ComputandoMetricas, BuildGraphCriadorCarteira, StateCarteira, 
import json
import logging
import pandas as pd
import datetime


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

graph_weights_build = BuildGraphCriadorCarteira()
graph_weights_build = graph_weights_build.compile()
tics = ["VALE3", "PETR4", "ITUB4", "BBDC4", "ABEV3", 
        "MGLU3", "BBAS3", "GGBR4", "RENT3", "LREN3",
        "PSSA3", "BRAP4", "VIVT3"]

sequencia_datas = sequencia_datas(start="2020-01-01", end="2025-12-31", freq="QS")

import time
from IPython.display import display, Markdown
results_dict = {}
results_dict_marcowitz = {}
for data_inicio, data_fim in sequencia_datas.items():
    display(Markdown(f"## Iniciando o processo para o periodo de {data_inicio} a {data_fim}"))
    try:
        start_time = time.time()
        results_tics = await run_all_tics(
            tics,
            data_inicio=data_inicio,
            data_fim=data_fim
            )
        
        logger.info(f"Avaliação das acoes foi concluído para {data_inicio} a {data_fim}")    
        
        dados_markdown = transformando_data_frame_para_markdown(results_tics)
        
        
        correlacao_tics = correlacao(list(results_tics.keys()))
        
        response_pesos = await graph_weights_build.ainvoke(
            StateCarteira({
            "justification" : "",
            "avaliacao_acoes": dados_markdown,
            "correlacao_acoes": correlacao_tics,
            "interacao" : 0,
            "tics" : tics
            }))
        
        results_dict[f"{data_inicio} a {data_fim}"] = response_pesos
        
        logger.info(f"O peso foi calculado para {data_inicio} a {data_fim}") 
        
        tics_selecionados = list(response_pesos['tickers_weights'].keys()) 
        
        pesos = list(response_pesos['tickers_weights'].values()) 
        
        pesos_pd = pd.DataFrame(response_pesos['tickers_weights'], index=["Carteira"]).T
        
        display(pesos_pd.style.set_caption("Pesos da Carteira").background_gradient(cmap="Blues"))
        
        tics_selecionados = [tics if ".SA" in tics else tics + ".SA" for tics in tics_selecionados]
        
        data_now = datetime.datetime.now().strftime("%Y-%m-%d")
        
        comp = ComputandoMetricas(data_fim, data_now, tics_selecionados, pesos, 1000)
        
        weights_markowitz, _ = comp.computando_marcowitz()
        
        computando_marcowitz = weights_markowitz.iloc[-1].to_dict()
        
        results_dict_marcowitz[f"{data_inicio} a {data_fim}"] = computando_marcowitz
        
        comp.print_results()

        logger.info(f"Metricas foram calculadas para {data_inicio} a {data_fim}")
        
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Tempo de execução para {data_inicio} a {data_fim}: {execution_time:.2f} segundos")
        
    except Exception as e:
        logger.error(f"Erro ao processar {data_inicio} a {data_fim}: {e}")
        
with open("carteiras_no_tempo_agente.json", "w") as f:
    json.dump(results_dict, f)
    
with open("carteiras_no_tempo_marcowitz.json", "w") as f:
    json.dump(results_dict_marcowitz, f)
    

