import asyncio
import logging
from typing import Any, Optional, Type

from pydantic import BaseModel

from .roteador_api_nvidia import RouterApiNvidia
from .roteador_cerebras import RouterCerebras
from .roteador_groq import RouterGroq
from .roteador_langchain_nvidia import RouterLangChainNvidia
from .roteador_openai_nvidia import RouterOpenaiNvidia

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)

logger = logging.getLogger(__name__)


class AllProvidersFailedError(Exception):
    """Exceção levantada quando todos os provedores LLM falham"""


class LlmRouter:
    def __init__(
        self,
        messages: str,
        strutured_output: Optional[Type[BaseModel]] = None,
        **kwargs,
    ):
        self.messages = messages
        self.strutured_output = strutured_output

        # Centraliza os modelos default
        self.models = {
            "Groq": kwargs.get(
                "groq_models",
                [
                    "moonshotai/kimi-k2-instruct-0905",
                    "meta-llama/llama-4-scout-17b-16e-instruct",
                    "openai/gpt-oss-120b",
                ],
            ),
            "Cerebras": kwargs.get(
                "cerebras_models",
                [
                    "qwen-3-235b-a22b-instruct-2507",
                    "gpt-oss-120b",
                    "qwen-3-32b",
                ],
            ),
            "API_Nvidia": kwargs.get(
                "api_nvidia_models",
                [
                    "nvidia/nemotron-3-nano-30b-a3b",
                    "moonshotai/kimi-k2-instruct",
                    "deepseek-ai/deepseek-v3.2",
                    "moonshotai/kimi-k2-instruct-0905",
                    "meta/llama-4-scout-17b-16e-instruct",
                    "qwen/qwen3-next-80b-a3b-instruct",
                ],
            ),
            "Langchain_nvidia": kwargs.get(
                "api_langchain_nvidia_models",
                [
                    "nvidia/nemotron-4-mini-hindi-4b-instruct",
                ],
            ),
            "Openai_nvidia": kwargs.get(
                "api_openai_nvidia_models",
                [
                    "qwen/qwen3-next-80b-a3b-instruct",
                    "deepseek-ai/deepseek-v3.2",
                    "nvidia/nemotron-3-nano-30b-a3b",
                    "moonshotai/kimi-k2-instruct",
                    "nvidia/nemotron-4-mini-hindi-4b-instruct",
                ],
            ),
        }

    async def _try_provider(
        self, provider_name: str, router_class: Type, method_name: str
    ) -> Any:
        """
        Método genérico para tentar modelos de um provedor específico.
        """
        models = self.models.get(provider_name, [])
        for model in models:
            logger.info("Tentando %s %s", provider_name, model)
            try:
                router = router_class(self.messages, model, self.strutured_output)

                func = getattr(router, method_name)
                result = await func() if asyncio.iscoroutinefunction(func) else func()

                if result:
                    return result
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning("Falha no %s %s %s", provider_name, model, e)
                continue
        return None

    async def llm_router(self) -> Any:
        logger.info("Iniciando roteamento LLM")

        # Configuração dos provedores: (Nome, Classe do Roteador, Método a chamar)
        providers = [
            ("API_Nvidia", RouterApiNvidia, "ainvoke"),
            (
                "Langchain_nvidia",
                RouterLangChainNvidia,
                "llm_nvidia_structured" if self.strutured_output else "llm_nvidia",
            ),
            (
                "Groq",
                RouterGroq,
                "llm_structured_groq" if self.strutured_output else "llm_groq",
            ),
            (
                "Cerebras",
                RouterCerebras,
                (
                    "get_response_cerebras_structured_async"
                    if self.strutured_output
                    else "get_response_cerebras_async"
                ),
            ),
            (
                "Openai_nvidia",
                RouterOpenaiNvidia,
                (
                    "llm_structured_openai_nvidia"
                    if self.strutured_output
                    else "llm_openai_nvidia"
                ),
            ),
        ]

        errors = {}
        for name, cls, method in providers:
            try:
                logger.info("🔄 Rotando para provedor %s", name)
                response = await self._try_provider(name, cls, method)

                if response:
                    logger.info("✅ %s sucesso", name)
                    return response

                errors[name] = "Todos os modelos deste provedor falharam"
            except Exception as e:  # pylint: disable=broad-exception-caught
                errors[name] = str(e)

        raise AllProvidersFailedError(f"Falha total: {errors}")
