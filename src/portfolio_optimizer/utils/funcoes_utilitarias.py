import json
import logging
from typing import Any, Dict

import pandas as pd

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def tratando_resposta_router_llm(response: Any, model_class=None) -> Dict[Any, Any]:
    """
    Extrai os campos definidos na model_class (Pydantic) da resposta, independentemente do tipo retornado.
    """
    if hasattr(response, "output"):
        response = response.output

    if model_class and hasattr(response, "dict"):
        return response.dict()  # type: ignore

    if isinstance(response, dict):
        if model_class and hasattr(model_class, "__fields__"):
            return {field: response.get(field) for field in model_class.__fields__}
        return response

    if isinstance(response, str):
        try:
            response_json = json.loads(response)
            if model_class and hasattr(model_class, "__fields__"):
                return {
                    field: response_json.get(field) for field in model_class.__fields__
                }
            return response_json  # type: ignore
        except Exception:  # # pylint: disable=broad-exception-caught
            return {}

    if model_class and hasattr(model_class, "__fields__"):
        result = {}
        for field in model_class.__fields__:
            if hasattr(response, field):
                result[field] = getattr(response, field)
        if result:
            return result
    return {}


def normalizar_pesos(
    weights_dict: dict, target_sum: int = 100, tolerancia: float = 0.01
) -> dict:
    """
    Normaliza os pesos para somarem exatamente o target_sum.

    Args:
        weights_dict: Dicionário com os pesos {ticker: peso}
        target_sum: Soma alvo (padrão: 100)
        tolerancia: Tolerância para considerar soma correta (padrão: 0.01)

    Returns:
        Dicionário com pesos normalizados
    """
    total_atual = sum(weights_dict.values())
    diferenca = abs(total_atual - target_sum)

    # Se já está dentro da tolerância, retorna o original
    if diferenca <= tolerancia:
        logger.info(
            "✓ Pesos já somam total_atual = %.2f%% (dentro da tolerância)", total_atual
        )
        return weights_dict

    # Normalização proporcional (melhor que distribuir igualmente)
    fator_normalizacao = target_sum / total_atual
    weights_normalizados = {
        ticker: peso * fator_normalizacao for ticker, peso in weights_dict.items()
    }

    logger.warning(
        "⚠ Pesos ajustados: %.2f%% → %.2f%% (fator: %.4f)",
        total_atual,
        target_sum,
        fator_normalizacao,
    )

    soma_final = sum(weights_normalizados.values())
    logger.info("✓ Soma final: soma_final = %.4f%%", soma_final)

    return weights_normalizados


def transformando_data_frame_para_markdown(results):
    try:
        results_pd = pd.DataFrame.from_dict(results).T
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Erro ao transformar o dicionário em DataFrame: %s", e)
        results_pd = pd.DataFrame.from_dict(results, orient="index").T
    dados_markdown = (
        results_pd.loc[:, ["classification", "analysis"]]
        .reset_index()
        .rename(columns={"index": "tic"})
        .to_markdown()
    )
    return dados_markdown
