import asyncio
from typing import List

from langchain_docling.loader import DoclingLoader


class LinksExtractorDoclingLoaderAsync:
    def __init__(self, file_path: List[str]):
        self.file_path = file_path

    async def load(self, file_path: str) -> list:
        loader = DoclingLoader(file_path=file_path)
        docs = loader.load()
        return docs

    async def process_links(self, links: List[str]) -> str:
        async def process_single_link(link: str) -> str:
            try:
                docs = await self.load(link)
                content = docs[0].page_content
                return str(content) if content is not None else ""
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Erro ao carregar o link: {link} - {str(e)}")
                return ""

        # Processa todos os links em paralelo
        results = await asyncio.gather(
            *[process_single_link(link) for link in links], return_exceptions=False
        )

        # Combina os resultados
        documents = "/n/NEW NOTICE/n/".join(filter(None, results))

        return documents

    async def clear_process_links(self) -> List[str]:
        """
        Processa uma lista de links e retorna o conteúdo combinado.

        Args:
            links (List[str]): Lista de links a serem processados.

        Returns:
            str: Conteúdo combinado dos links processados.

        """
        response = await self.process_links(self.file_path)
        linhas_limpas = [
            linha.strip()
            for linha in response.split("\n")
            if "https" not in linha
            and "[" not in linha
            and len(linha.strip()) > 120
            and "*" not in linha
        ]
        return linhas_limpas
