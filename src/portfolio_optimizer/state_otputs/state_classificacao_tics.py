from typing import Literal, TypedDict


class StateClassification(TypedDict):
    classification: Literal["Excellent", "Good", "Fair", "Poor", "Very Poor"]
    analysis: str
    tic: str
    dados_fundamentalistas: str
    data_inicio: str
    data_fim: str
    avaliacao_analise: str
    description_avaliacao_analise: str
    interacao: int
