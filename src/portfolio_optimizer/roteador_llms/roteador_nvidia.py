import logging
from typing import Any, Optional

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RouterNvidia:
    def __init__(
        self,
        messages: str,
        model_llm: str,
        strutured_output: Optional[BaseModel] = None,
    ):
        self.messages = messages
        self.model_llm = model_llm
        self.strutured_output = strutured_output

    async def llm_nvidia(self) -> Optional[str]:
        """
        Chama modelo Nvidia via LangChain
        """
        try:
            llm = ChatNVIDIA(model=self.model_llm)
            response = await llm.ainvoke([{"role": "user", "content": self.messages}])
            return response.content  # type:ignore

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Erro no llm_nvidia: %s", e)
            raise

    async def llm_nvidia_structured(self) -> Optional[Any] | BaseModel:
        """
        Chama modelo Nvidia via LangChain com saída estruturada
        """
        if self.strutured_output is None:
            raise ValueError(
                "structured_output precisa estar definido para usar essa função."
            )

        try:
            llm = ChatNVIDIA(model=self.model_llm)
            llm_strutured = llm.with_structured_output( # type:ignore
                self.strutured_output  # type:ignore
            )

            response = await llm_strutured.ainvoke(  # type:ignore
                [{"role": "user", "content": self.messages}]
            )  # type:ignore
            
            if response is None:
                logger.warning(f"Resposta nula recebida do modelo Nvidia. O modelo {self.model_llm} pode não suportar saída estruturada.")
            
            return response  # type:ignore

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Erro no llm_nvidia_structured: %s", e)
            raise