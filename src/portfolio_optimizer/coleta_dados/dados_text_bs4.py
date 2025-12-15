import warnings
from typing import Optional

import httpx
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")


class LinksExtractorBS4:
    def get_text_from_url(self, url: str) -> Optional[str]:
        """
        Fetches the HTML content from a given URL, parses it using BeautifulSoup,
        and extracts the text content, removing HTML tags.

        Args:
            url: The URL to fetch and parse.

        Returns:
            A string containing the extracted text content, or None if an error occurs.
        """
        try:
            response = httpx.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract text content while ignoring script and style tags
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()

            # Break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = "\n".join(chunk for chunk in chunks if chunk)

            return text

        except httpx.HTTPError as e:
            print(f"Error fetching URL: {e}")
            return None

    def clean_text_bs4(self, url: str) -> Optional[str]:
        scrape_result = self.get_text_from_url(url)
        if isinstance(scrape_result, str):
            linhas = scrape_result.split("\n")
        else:
            return None

        # Remover links, linhas vazias, linhas com colchetes e linhas curtas
        linhas_limpas = [
            linha.strip()
            for linha in linhas
            if "https" not in linha
            and "[" not in linha
            and len(linha.strip()) > 50
            and "*" not in linha
        ]

        return "\n".join(linhas_limpas)
