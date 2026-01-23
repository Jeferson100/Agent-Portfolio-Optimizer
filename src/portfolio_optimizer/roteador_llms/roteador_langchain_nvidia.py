import logging
from typing import Any, Optional

from langchain_nvidia_ai_endpoints import ChatNVIDIA  # pylint: disable=import-error
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)

logger = logging.getLogger(__name__)


class RouterLangChainNvidia:
    def __init__(
        self,
        messages: str,
        model_llm: str,
        strutured_output: Optional[BaseModel] = None,
    ):
        self.messages = messages
        self.model_llm = model_llm
        self.strutured_output = strutured_output

    # @retry(stop_max_attempt_number=2, wait_fixed=2000)
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

    # @retry(stop_max_attempt_number=2, wait_fixed=2000)
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
            llm_strutured = llm.with_structured_output(  # type:ignore
                self.strutured_output  # type:ignore
            )

            response = await llm_strutured.ainvoke(  # type:ignore
                [{"role": "user", "content": self.messages}]
            )  # type:ignore

            if response is None:
                logger.warning(
                    "Resposta nula recebida do modelo Nvidia. O modelo model_llm=%s pode não suportar saída estruturada.",
                    self.model_llm,
                )

            return response  # type:ignore

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Erro no llm_nvidia_structured: %s", e)
            raise
