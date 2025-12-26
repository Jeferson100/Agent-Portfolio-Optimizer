import json
import logging
from utils import ComputandoMetricas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open("../data/carteira_resultado.json", "r") as f:
    carteira_resultado = json.load(f)

logger.info("Dados da carteira carregados com sucesso. Iniciando computação de métricas...")
    
comp = ComputandoMetricas("2025-01-01", "2025-12-31",carteira_resultado['tickers_weights'] ,100000)

comp.print_results(save_path="../data/")

logger.info("Métricas computadas e salvas com sucesso.")
    

