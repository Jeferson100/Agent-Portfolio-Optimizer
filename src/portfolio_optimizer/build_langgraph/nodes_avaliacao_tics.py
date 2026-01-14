import asyncio
from typing import Any, Dict, Literal

from ..prompts.prompts_avaliador_tics import PROMPT_ANALISE, PROMPT_AVALIADOR
from ..roteador_llms.roteador_llms import LlmRouter
from ..state_otputs.output_classicacao_tics import SeniorAvaliador, TickerLevel
from ..tratando_dados.tratando_dados_fundamentalistas import (
    TratandoDadosFundamentalistas,
)
from ..utils.funcoes_utilitarias import tratando_resposta_router_llm

import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logger = logging.getLogger(__name__)


async def get_data_fundamentalistas(state) -> Dict[str, str]:
    tic = state.get("tic")

    data_inicio = state.get("data_inicio")

    data_fim = state.get("data_fim")

    trat = TratandoDadosFundamentalistas(tic, data_inicio, data_fim)

    dados = await trat.coleta_dados_fundamentalistas()

    dados_markdow = dados.to_markdown()
    
    logger.info("Dados fundamentais coletados com sucesso")

    return {"dados_fundamentalistas": str(dados_markdow)}


async def analista_fundamentalista(state) -> Dict[Any, Any]:
    data = state.get("dados_fundamentalistas")

    description_avaliacao_analise = state.get("description_avaliacao_analise")

    prompt_formatted = PROMPT_ANALISE.format(
        fundamentos=data, description_avaliacao_analise=description_avaliacao_analise
    )
    llm = LlmRouter(
        prompt_formatted,
        strutured_output=TickerLevel,  # type:ignore
    )

    response = await llm.llm_router()

    response_trat = tratando_resposta_router_llm(response, TickerLevel)
    
    logger.info("Analise fundamentalista feita com sucesso")

    await asyncio.sleep(2)

    return {
        "classification": response_trat.get("classification"),
        "analysis": response_trat.get("analysis"),
    }


async def avaliador_analista_fundamentalista(state) -> Dict[Any, Any]:
    data = state.get("dados_fundamentalistas")
    classification = state.get("classification")
    analise = state.get("analysis")
    interacao = state.get("interacao", 0)

    prompt_formatted = PROMPT_AVALIADOR.format(
        fundamentos=data, classification=classification, analise=analise
    )

    llm = LlmRouter(
        prompt_formatted,
        strutured_output=SeniorAvaliador,  # type:ignore
    )

    response = await llm.llm_router()
    
    logger.info("Avaliador da analise fundamentalista feito com sucesso")

    await asyncio.sleep(2)

    response_trat = tratando_resposta_router_llm(response, SeniorAvaliador)

    new_interacao = interacao + 1

    return {
        "avaliacao_analise": response_trat.get("avaliacao_analise"),
        "description_avaliacao_analise": response_trat.get(
            "description_avaliacao_analise"
        ),
        "interacao": new_interacao,
    }


def should_continue(state) -> Literal["END", "analise_fundamentalista"]:
    avaliacao = state.get("avaliacao_analise")
    interacao = state.get("interacao")
    logger.info(f"Avaliacao: {avaliacao}, Interacao: {interacao}")
    if avaliacao or interacao >= 4:
        return "END"
    return "analise_fundamentalista"
