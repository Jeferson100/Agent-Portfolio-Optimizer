import asyncio
import logging
from typing import Any, Optional, Type

from pydantic import BaseModel

from .roteador_api_nvidia import RouterApiNvidia
from .roteador_cerebras import RouterCerebras
from .roteador_groq import RouterGroq
from .roteador_huggingface import RouterPydanticAI
from .roteador_langchain_nvidia import RouterLangChainNvidia
from .roteador_openai_nvidia import RouterOpenaiNvidia

logging.basicConfig(level=logging.INFO)

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
                    "OpenAI GPT OSS",
                    "qwen-3-32b",
                ],
            ),
            "API_Nvidia": kwargs.get(
                "api_nvidia_models",
                [
                    "deepseek-ai/deepseek-v3.2",
                    "nvidia/nemotron-3-nano-30b-a3b",
                    "moonshotai/kimi-k2-instruct",
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
            logger.info(f"Tentando {provider_name}: {model}")
            try:

                router = router_class(self.messages, model, self.strutured_output)

                func = getattr(router, method_name)
                result = await func() if asyncio.iscoroutinefunction(func) else func()

                if result:
                    return result
            except Exception as e:
                logger.warning(f"Falha no {provider_name} ({model}): {e}")
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
                logger.info(f"🔄 Rotando para provedor: {name}")
                response = await self._try_provider(name, cls, method)

                if response:
                    logger.info(f"✅ {name} sucesso")
                    return response

                errors[name] = "Todos os modelos deste provedor falharam"
            except Exception as e:
                errors[name] = str(e)

        raise AllProvidersFailedError(f"Falha total: {errors}")


""""class LlmRouter:
    

    def __init__(
        self,
        messages: str,
        strutured_output: Optional[BaseModel] = None,
        groq_models: Optional[list[str]] = None,
        huggingface_models: Optional[list[str]] = None,
        langachain_nvidia_models: Optional[list[str]] = None,
        cerebras_models: Optional[list[str]] = None,
        openai_nvidia_models: Optional[list[str]] = None,
        api_nvidia_models: Optional[list[str]] = None,
    ):
        self.messages = messages
        self.strutured_output = strutured_output
        self.groq_models = groq_models or [
            "moonshotai/kimi-k2-instruct-0905",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "openai/gpt-oss-120b",
        ]

        self.huggingface_models = huggingface_models or [
            "Qwen/Qwen3-235B-A22B-Instruct-2507",
            "microsoft/DialoGPT-large",
            "meta-llama/Llama-4-Maverick-17B-128E",
        ]

        self.langchain_nvidia_models = langachain_nvidia_models or [
            #"nvidia/nemotron-4-mini-hindi-4b-instruct",
            "moonshotai/kimi-k2-instruct-0905",
            "qwen/qwen3-235b-a22b",
            "qwen/qwen3-next-80b-a3b-instruct",
            "deepseek-ai/deepseek-v3.2",
            "nvidia/nemotron-3-nano-30b-a3b",
            "moonshotai/kimi-k2-instruct",
        ]
        self.cerebras_models = cerebras_models or [
            "qwen-3-235b-a22b-instruct-2507",
            "gpt-oss-120b",
            "OpenAI GPT OSS",
            "qwen-3-32b",
               
        ]
        self.openai_nvidia_models = openai_nvidia_models or [
            "qwen/qwen3-next-80b-a3b-instruct",
            "deepseek-ai/deepseek-v3.2",
            "nvidia/nemotron-3-nano-30b-a3b",
            "moonshotai/kimi-k2-instruct",
            "nvidia/nemotron-4-mini-hindi-4b-instruct",
        ]
        self.api_nvidia_models = api_nvidia_models or [
            "moonshotai/kimi-k2-instruct-0905",
            "qwen/qwen3-next-80b-a3b-instruct",
            "deepseek-ai/deepseek-v3.2",
            "nvidia/nemotron-3-nano-30b-a3b",
            "moonshotai/kimi-k2-instruct",
            "meta/llama-4-scout-17b-16e-instruct",
        ]

    async def try_groq_models(self) -> Dict[str, Any] | str | None:
        
        for model in self.groq_models:
            logger.info("Tentando modelo Groq: %s", model)
            try:
                llm_response = RouterGroq(self.messages, model, self.strutured_output)

                if self.strutured_output:
                    result = await llm_response.llm_structured_groq()
                else:
                    result = await llm_response.llm_groq()  # type:ignore
                return result
    
            except (ConnectionError, TimeoutError, ValueError) as e:
                logger.warning("Falha no modelo Groq %s: %s", model, e)
                continue
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning("Falha no modelo Groq %s: %s", model, e)
                continue
        return None

    async def try_huggingface_models(self) -> Any:
        
        for model in self.huggingface_models:
            try:
                llm_response = RouterPydanticAI(
                    self.messages, model, self.strutured_output
                )

                if self.strutured_output:
                    result = await llm_response.llm_structured_pydanticai()
                else:
                    result = await llm_response.llm_pydanticai()
            
                return result

            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Falha no modelo Huggingface %s: %s", model, e)
                continue

    async def try_langchain_nvidia_models(self) -> Any:
        
        for model in self.langchain_nvidia_models:
            try:
                llm_response = RouterLangChainNvidia(self.messages, model, self.strutured_output)

                if self.strutured_output:
                    result = await llm_response.llm_nvidia_structured()
                else:
                    result = await llm_response.llm_nvidia()
                
                return result

            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Falha no modelo Langchain Nvidia %s: %s", model, e)
                continue
            
    async def try_openai_nvidia_models(self) -> Any:
        
        for model in self.openai_nvidia_models:
            try:
                llm_response = RouterOpenaiNvidia(self.messages, model, self.strutured_output)

                if self.strutured_output:
                    result = await llm_response.llm_structured_openai_nvidia()
                else:
                    result = await llm_response.llm_openai_nvidia()
                
                return result

            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Falha no modelo Openai Nvidia %s: %s", model, e)
                continue
    

    async def try_cerebras_models(self) -> Any:  # type: ignore
       
        for model in self.cerebras_models:
            try:
                llm_response = RouterCerebras(
                    self.messages, model, self.strutured_output
                )

                if self.strutured_output:
                    result = await llm_response.get_response_cerebras_structured_async()
                else:
                    result = await llm_response.get_response_cerebras_async()  # type:ignore
                
                return result

            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Falha no modelo Cerebras %s: %s", model, e)
                continue
        return None

    async def try_api_nvidia_models(self) -> Any:
       
        for model in self.api_nvidia_models:
            try:
                llm_response = RouterApiNvidia(model)

                if self.strutured_output:
                    result = await llm_response.ainvoke(self.messages, schema=self.strutured_output)
                else:
                    result = await llm_response.ainvoke(self.messages)
                
                return result

            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Falha no modelo API Nvidia %s: %s", model, e)
                continue
    
    

    async def llm_router(self) -> Union[Dict[str, Any], str, Any]:
       
        logger.info("Iniciando roteamento LLM")

        providers = [
            ("Langchain_Nvidia", self.try_langchain_nvidia_models),
            ("API_Nvidia", self.try_api_nvidia_models),
            #("Openai_Nvidia", self.try_openai_nvidia_models),
            ("Cerebras", self.try_cerebras_models),
            ("Groq", self.try_groq_models),
            ("HuggingFace", self.try_huggingface_models),
        ]

        errors = {}

        for provider_name, provider_func in providers:
            try:
                logger.info("🔄 Tentando provider_name=%s...", provider_name)
                response = await provider_func()

                if response is not None:
                    logger.info(
                        "✅ provider_name=%s respondeu com sucesso", provider_name
                    )
                    return response

                error_msg = f"{provider_name} retornou None"
                logger.warning("⚠️ error_msg=%s", error_msg)
                errors[provider_name] = error_msg

            except Exception as e:  # pylint: disable=broad-except
                error_msg = str(e)
                logger.warning(
                    "❌ provider_name=%s falhou: error_msg=%s", provider_name, error_msg
                )
                errors[provider_name] = error_msg

        # Se todos falharam
        error_summary = " | ".join([f"{k}: {v}" for k, v in errors.items()])
        raise AllProvidersFailedError(
            f"Todos os provedores falharam ou retornaram None. Detalhes: {error_summary}"
        )
"""
