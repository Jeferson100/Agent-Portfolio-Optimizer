import logging
from typing import Literal

from ..prompts.prompts_criador_carteira import (
    PROMPT_AVALIADOR_PESOS_CARTEIRA,
    PROMPT_CRIANDO_CARTEIRA,
    RECOMENDACAO_SENIOR,
)
from ..roteador_llms.roteador_llms import LlmRouter
from ..state_otputs.output_criador_carteira import CarteiraWeights
from ..utils import normalizar_pesos, tratando_resposta_router_llm
import time

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def analista_criador_carteira(state):
    correlacao = state.get("correlacao_acoes")

    dados_markdown = state.get("avaliacao_acoes")

    analise_avaliador_weights = state.get("analise_avaliador_weights")

    soma_pesos_error = state.get("soma_weights_error")

    tics_error = state.get("tics_error")

    recomendacao = (
        RECOMENDACAO_SENIOR.format(recomendacao=analise_avaliador_weights)
        if analise_avaliador_weights
        else ""
    )

    soma_pesos_error = soma_pesos_error or ""

    tics_error = tics_error or ""

    PROMPT_CRIANDO_CARTEIRA_FORMATED = PROMPT_CRIANDO_CARTEIRA.format(
        classificacoes_acoes=dados_markdown,
        matriz_correlacao=correlacao,
        recomendacao=recomendacao,
        soma_pesos_error=soma_pesos_error,
        tics_error=tics_error,
    )

    llm = LlmRouter(PROMPT_CRIANDO_CARTEIRA_FORMATED, CarteiraWeights)  # type:ignore

    response = await llm.llm_router()
    
    time.sleep(2)

    response_trat = tratando_resposta_router_llm(response, CarteiraWeights)

    return {
        "tickers_weights": response_trat.get("tickers_weights"),
        "justification": response_trat.get("justification"),
    }


async def analista_avaliador_peso_carteira(state):
    alocacao_proposta = state.get("tickers_weights")

    justificativa = state.get("justification")

    correlacao = state.get("correlacao_acoes")

    dados_markdown = state.get("avaliacao_acoes")

    interacao = state.get("interacao", 0)

    soma_pesos_error = state.get("soma_weights_error")

    tics_disponiveis = state.get("tics")

    tics_disponiveis_sa = [
        tic if tic.endswith(".SA") else tic + ".SA" for tic in tics_disponiveis
    ]

    soma_pesos_error = soma_pesos_error or ""

    PROMPT_AVALIADOR_PESOS_CARTEIRA_FORMATTED = PROMPT_AVALIADOR_PESOS_CARTEIRA.format(
        alocacao_proposta=alocacao_proposta,
        justificativa=justificativa,
        classificacoes_acoes=dados_markdown,
        matriz_correlacao=correlacao,
        soma_pesos_error=soma_pesos_error,
        tickers_disponiveis=tics_disponiveis_sa,
    )

    llm = LlmRouter(
        PROMPT_AVALIADOR_PESOS_CARTEIRA_FORMATTED,
    )
    response = await llm.llm_router()
    
    time.sleep(2)

    new_interacao = interacao + 1

    return {"analise_avaliador_weights": response, "interacao": new_interacao}


async def verify_weight_sum(state):
    """
    Verifica e normaliza a soma dos pesos do portfólio.
    """
    weights = state.get("tickers_weights")

    # Verificação de entrada
    if not weights:
        return {
            "soma_weights_error": "⚠️ Nenhum peso de ticker fornecido.",
            "tickers_weights": {},
        }

    # Normalizar pesos
    new_pesos = normalizar_pesos(weights)

    # CORREÇÃO: Adicionar () para chamar o método
    sum_new_pesos = sum(new_pesos.values())

    # Verificar se ainda há erro após normalização
    if abs(sum_new_pesos - 100) > 0.01:
        erro_percentual = abs(sum_new_pesos - 100.0)

        return {
            "soma_weights_error": f"""<🚨 PREVIOUS ALLOCATION ERROR DETECTED>
            Your last attempt produced a total weight of **{sum_new_pesos:.2f}%** instead of 100.00%.
            This is an error of **{erro_percentual:.2f} percentage points**.

            **Original weights:** {weights}
            **After normalization:** {new_pesos}
            **Sum after normalization:** {sum_new_pesos:.4f}%

            Please review and provide corrected weights.
            </🚨 PREVIOUS ALLOCATION ERROR DETECTED>""",
            "tickers_weights": weights,  # Retorna original em caso de erro
        }

    # Sucesso
    logger.info("✓ Pesos normalizados com sucesso: soma = %s", sum_new_pesos)
    return {"soma_weights_error": None, "tickers_weights": new_pesos}


def verifica_tics_selecionados(state):
    tics_pesos = state.get("tickers_weights")

    tics_possiveis = state.get("tics")

    tics_possiveis_sem_sa = [tic.split(".")[0] for tic in tics_possiveis]

    tics_pesos_sem_sa = [tic.split(".")[0] for tic in tics_pesos.keys()]

    tics_modelo = list(tics_pesos_sem_sa)

    tics_comparados = [tic for tic in tics_modelo if tic not in tics_possiveis_sem_sa]

    if tics_comparados:
        tics_comparados_s = ",".join(tics_comparados)
        logger.info(
            "Os seguintes tickers não foram encontrados: tics_comparados_s = %s",
            tics_comparados_s,
        )
        return {
            "tics_error": f"""
                                <🚨 PREVIOUS TICKER SELECTION ERROR DETECTED:**>
                                
                                Your last attempt produced one tickers error.
        
                                The following tickers were not found: {tics_comparados_s}

                                Please ensure that:
                                - Ticker symbols are spelled correctly
                                - Assets exist in the database
                                - There are no extra spaces or invalid character 
                                
                                Please try again with valid tickers.
                                
                                </🚨 PREVIOUS TICKER SELECTION ERROR DETECTED:**>
                                """
        }

    return {"tics_error": None}


def should_continue(state) -> Literal["END", "analista_avaliador_peso_carteira"]:
    MAX_ITERATIONS = 3

    interacao = state.get("interacao")

    tics_error = state.get("tics_error")

    max_iterations_reached = interacao >= MAX_ITERATIONS

    no_ticker_errors = tics_error is None

    if max_iterations_reached and no_ticker_errors:
        return "END"
    return "analista_avaliador_peso_carteira"
