import os
import json
import re
import logging
import requests
from typing import Optional, Type, TypeVar, Any
from pydantic import BaseModel, ValidationError
import httpx
from retrying import retry


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#T = TypeVar("T", bound=BaseModel)

class RouterApiNvidia:
    def __init__(self, messages: str, model_llm: str, strutured_output: Optional[BaseModel] = None):
        self.messages = messages
        self.model_llm = model_llm
        self.strutured_output = strutured_output
        self.api_key = os.getenv('NVIDIA_API_KEY')
        self.base_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.session = requests.Session()
        
        
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY não encontrada nas variáveis de ambiente.")

    @property
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

    def _extract_json(self, text: str) -> str:
        """Extrai o conteúdo JSON de dentro de blocos de código markdown, se existirem."""
        pattern = r"```json\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else text.strip()

    #@retry(stop_max_attempt_number=2, wait_fixed=2000)
    def invoke(self) -> Any:
        """
        Método unificado. Se schema for passado, retorna objeto Pydantic.
        Caso contrário, retorna string.
        """
        payload = {
            "model": self.model_llm,
            "messages": [],
            "temperature": 0.1 # Baixa temperatura para saídas estruturadas
        }

        if self.strutured_output:

            payload["messages"].append({
                "role": "system",
                "content": f"Respond EXCLUSIVELY in JSON. Schema: {json.dumps(self.strutured_output.model_json_schema())}"
            })
        
        payload["messages"].append({"role": "user", "content": self.messages})

        try:
            response = self.session.post(
                self.base_url, 
                headers=self._headers, 
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']

            if self.strutured_output:
                clean_json = self._extract_json(content)
                return self.strutured_output.model_validate_json(clean_json)
            
            return content

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na chamada da API: {e}")
            return None
        except (ValidationError, json.JSONDecodeError) as e:
            logger.error(f"Erro ao processar formato estruturado: {e}")
            return None
        
    #@retry(stop_max_attempt_number=2, wait_fixed=2000)
    async def ainvoke(self) -> Any:
        """
        Versão assíncrona do método invoke.
        """
        payload = {
            "model": self.model_llm,
            "messages": [],
            "temperature": 0.1
        }

        if self.strutured_output:
            payload["messages"].append({
                "role": "system",
                "content": f"Respond EXCLUSIVELY in JSON. Schema: {json.dumps(self.strutured_output.model_json_schema())}"
            })
        
        payload["messages"].append({"role": "user", "content": self.messages})
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    self.base_url, 
                    headers=self._headers, 
                    json=payload
                )
                response.raise_for_status()
                
                content = response.json()['choices'][0]['message']['content']

                if self.strutured_output:
                    clean_json = self._extract_json(content)
                    return self.strutured_output.model_validate_json(clean_json)
                
                return content

            except httpx.HTTPStatusError as e:
                logger.error(f"Erro HTTP: {e.response.status_code} - {e.response.text}")
                return None
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")
                return None
