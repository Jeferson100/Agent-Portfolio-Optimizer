import json
import logging
from typing import Any, Dict, Optional

from groq import AsyncGroq
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
logger = logging.getLogger(__name__)

client = AsyncGroq()


class RouterGroq:
    def __init__(
        self,
        messages: str,
        model_llm: str,
        strutured_output: Optional[BaseModel] = None,
    ):
        self.messages = messages
        self.strutured_output = strutured_output
        self.model_llm = model_llm

    async def llm_structured_groq(self) -> Dict[str, Any] | None:
        """
        Chama modelo Groq com saída estruturada

        """

        if self.strutured_output is None:
            raise ValueError(
                "structured_output precisa estar definido para usar essa função."
            )
        try:
            response = await client.chat.completions.create(  # type: ignore[no-matching-overload]
                model=self.model_llm,
                messages=[
                    {"role": "user", "content": self.messages},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "structured_response",
                        "schema": self.strutured_output.model_json_schema(),
                    },
                },
            )
            content = response.choices[0].message.content or "{}"
            return json.loads(content)  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Erro ao chamar modelo Groq com saída estruturada: %s", e)
        return None

    async def llm_groq(self) -> str:
        """
        Chama modelo Groq sem saída estruturada
        """
        response = await client.chat.completions.create(  # type: ignore[no-matching-overload]
            model=self.model_llm,
            messages=[
                {"role": "user", "content": self.messages},
            ],
        )
        return response.choices[0].message.content or ""
