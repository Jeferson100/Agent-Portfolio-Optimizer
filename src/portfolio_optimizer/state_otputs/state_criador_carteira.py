from typing import Dict, List, TypedDict


class StateCarteira(TypedDict):
    tickers_weights: Dict[str, float]
    justification: str
    analise_avaliador_weights: str
    avaliacao_acoes: str
    correlacao_acoes: str
    interacao: int
    soma_weights_error: str
    tics: List[str]
    tics_error: str
