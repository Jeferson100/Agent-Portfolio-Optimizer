import logging
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent  # pylint: disable=E0401,E0611

# pylint: disable=E0401,E0611 #type:ignore;
from pydantic_ai.models.huggingface import (
    HuggingFaceModel,
)  # pylint: disable=E0401,E0611 #type:ignore;

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
logger = logging.getLogger(__name__)


class RouterPydanticAI:
    def __init__(
        self,
        messages: str,
        model_llm: str,
        strutured_output: Optional[BaseModel] = None,
    ):
        self.messages = messages
        self.strutured_output = strutured_output
        self.model_llm = model_llm

    async def llm_structured_pydanticai(self) -> Any:
        """
        Chama modelo HuggingFace via Pydantic AI com saída estruturada
        """
        try:
            if self.strutured_output is None:
                raise ValueError(
                    "structured_output precisa estar definido para usar essa função."
                )

            model = HuggingFaceModel(self.model_llm)
            agent = Agent(model, output_type=self.strutured_output)  # type:ignore

            response = agent.run_sync(self.messages)

            return response

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Erro no llm_pydantic_structured: %s", e)
            raise

    async def llm_pydanticai(self) -> Any:
        """
        Chama modelo HuggingFace via Pydantic AI sem saída estruturada
        """
        try:
            model = HuggingFaceModel(self.model_llm)
            agent = Agent(model)

            response = agent.run_sync(self.messages)

            return response

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Erro no llm_pydanticai: %s", e)
            raise
