import logging
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel

from .roteador_cerebras import RouterCerebras
from .roteador_groq import RouterGroq
from .roteador_huggingface import RouterPydanticAI
from .roteador_nvidia import RouterNvidia

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class AllProvidersFailedError(Exception):
    """Exceção levantada quando todos os provedores LLM falham"""


class LlmRouter:
    """
    Classe para roteamento automático entre diferentes modelos LLM com fallback
    """

    def __init__(
        self,
        messages: str,
        strutured_output: Optional[BaseModel] = None,
        groq_models: Optional[list[str]] = None,
        huggingface_models: Optional[list[str]] = None,
        nvidia_models: Optional[list[str]] = None,
        cerebras_models: Optional[list[str]] = None,
    ):
        self.messages = messages
        self.strutured_output = strutured_output
        self.groq_models = groq_models or [
            "moonshotai/kimi-k2-instruct-0905",
            "moonshotai/kimi-k2-instruct",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "openai/gpt-oss-120b",
        ]

        self.huggingface_models = huggingface_models or [
            "Qwen/Qwen3-235B-A22B-Instruct-2507",
            "microsoft/DialoGPT-large",
            "meta-llama/Llama-4-Maverick-17B-128E",
        ]

        self.nvidia_models = nvidia_models or [
            "qwen/qwq-32b",
            "moonshotai/kimi-k2-instruct",
            "openai/gpt-oss-20b",
            "microsoft/phi-4-mini-instruct",
            "nvidia/nemotron-4-mini-hindi-4b-instruct",
        ]
        self.cerebras_models = cerebras_models or [
            "qwen-3-235b-a22b-instruct-2507",
            "gpt-oss-120b",
            "llama-4-scout-17b-16e-instruct",
            "qwen-3-32b",
            # "llama3.1-8b",
            "llama-4-maverick-17b-128e-instruct",
        ]

    async def try_groq_models(self) -> Optional[Union[Dict[str, Any], str]]:
        """
        Tenta usar modelos Groq em ordem de prioridade
        """
        for model in self.groq_models:
            logger.info("Tentando modelo Groq: %s", model)
            try:
                llm_response = RouterGroq(self.messages, model, self.strutured_output)

                if self.strutured_output:
                    result = await llm_response.llm_structured_groq()
                else:
                    result = await llm_response.llm_groq()

                logger.info("Sucesso com modelo Groq: %s", model)
                return result
            except (ConnectionError, TimeoutError, ValueError) as e:
                logger.warning("Falha no modelo Groq %s: %s", model, e)
                continue
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning("Falha no modelo Groq %s: %s", model, e)
                continue

    async def try_huggingface_models(self) -> Any:
        """
        Tenta usar modelos HuggingFace em ordem de prioridade
        """
        for model in self.huggingface_models:
            try:
                llm_response = RouterPydanticAI(
                    self.messages, model, self.strutured_output
                )

                if self.strutured_output:
                    result = await llm_response.llm_structured_pydanticai()
                else:
                    result = await llm_response.llm_pydanticai()

                logger.info("Sucesso com modelo HuggingFace: %s", model)
                return result

            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Falha no modelo Huggingface %s: %s", model, e)
                continue

    async def try_nvidia_models(self) -> Any:
        """
        Tenta usar modelos Nvidia em ordem de prioridade
        """
        for model in self.nvidia_models:
            try:
                llm_response = RouterNvidia(self.messages, model, self.strutured_output)

                if self.strutured_output:
                    result = await llm_response.llm_nvidia_structured()
                else:
                    result = await llm_response.llm_nvidia()

                logger.info("Sucesso com modelo Nvidia: %s", model)
                return result

            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Falha no modelo Nvidia %s: %s", model, e)
                continue

    async def try_cerebras_models(self) -> Any:
        """
        Tenta usar modelos Cerebras em ordem de prioridade
        """
        for model in self.cerebras_models:
            try:
                llm_response = RouterCerebras(
                    self.messages, model, self.strutured_output
                )

                if self.strutured_output:
                    result = await llm_response.get_response_cerebras_structured_async()
                else:
                    result = await llm_response.get_response_cerebras_async()

                logger.info("Sucesso com modelo Cerebras: %s", model)

                return result

            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Falha no modelo Cerebras %s: %s", model, e)
                continue

    async def llm_router(self) -> Union[Dict[str, Any], str, Any]:
        """
        Método principal que implementa o sistema de fallback
        """
        logger.info("Iniciando roteamento LLM")

        providers = [
            ("Nvidia", self.try_nvidia_models),
            ("Cerebras", self.try_cerebras_models),
            ("Groq", self.try_groq_models),
            ("HuggingFace", self.try_huggingface_models),
        ]

        errors = {}

        for provider_name, provider_func in providers:
            try:
                logger.info("🔄 Tentando provider_name=%s...",provider_name)
                response = await provider_func()

                if response is not None:
                    logger.info("✅ provider_name=%s respondeu com sucesso", provider_name)
                    return response

                error_msg = f"{provider_name} retornou None"
                logger.warning("⚠️ error_msg=%s", error_msg)
                errors[provider_name] = error_msg

            except Exception as e: # pylint: disable=broad-except
                error_msg = str(e)
                logger.warning("❌ provider_name=%s falhou: error_msg=%s", provider_name, error_msg)
                errors[provider_name] = error_msg

        # Se todos falharam
        error_summary = " | ".join([f"{k}: {v}" for k, v in errors.items()])
        raise AllProvidersFailedError(
            f"Todos os provedores falharam ou retornaram None. Detalhes: {error_summary}"
        )
