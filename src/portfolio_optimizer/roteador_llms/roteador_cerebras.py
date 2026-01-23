import logging
import os
from typing import Optional

from cerebras.cloud.sdk import AsyncCerebras  # pylint: disable=E0401,E0611
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)

logger = logging.getLogger(__name__)


class RouterCerebras:
    def __init__(
        self,
        messages: str,
        model_llm: str,
        strutured_output: Optional[BaseModel] = None,
    ):
        self.messages = messages
        self.model_llm = model_llm
        self.strutured_output = strutured_output
        self.client_cerebras = self._get_client()

    def _get_client(self) -> AsyncCerebras:
        api_key = os.getenv("CEREBRAS_API_KEY")
        if not api_key:
            raise ValueError(
                "CEREBRAS_API_KEY não está definida nas variáveis de ambiente."
            )
        return AsyncCerebras(api_key=api_key)

    async def get_response_cerebras_structured_async(self) -> Optional[BaseModel]:
        if self.strutured_output is None:
            raise ValueError(
                "structured_output precisa estar definido para usar essa função."
            )
        try:
            response = await self.client_cerebras.chat.completions.create(
                model=self.model_llm,
                messages=[{"role": "user", "content": self.messages}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "structured_response",
                        "schema": self.strutured_output.model_json_schema(),
                    },
                },
            )
            return response.choices[0].message.content  # type:ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Erro no Cerebras: %s", e)
            raise

    async def get_response_cerebras_async(self) -> str:
        try:
            response = await self.client_cerebras.chat.completions.create(
                model=self.model_llm,
                messages=[{"role": "user", "content": self.messages}],
            )
            return response.choices[0].message.content  # type:ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Erro no Cerebras: %s", e)
            raise
