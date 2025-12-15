import asyncio
import warnings
from typing import Dict, List, Optional

import unidecode
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    SessionNotCreatedException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

warnings.filterwarnings("ignore")


class DadosNoticiasBuscadorYahooAsync:
    def __init__(self, acao: str, options: Options, tipo: str = "relevancia") -> None:
        self.acao = acao
        self.options = options
        self.tipo = tipo

    def service_chromium(self) -> Service:
        svc = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        return svc

    def service_chrome(self) -> Service:
        svc = Service(ChromeDriverManager().install())
        return svc

    async def navegador_get(self) -> webdriver.Chrome:
        try:
            navegador = webdriver.Chrome(
                service=self.service_chromium(), options=self.options
            )
        except SessionNotCreatedException:
            navegador = webdriver.Chrome(
                service=self.service_chrome(), options=self.options
            )
        navegador.get("https://br.search.yahoo.com/?fr2=p:fprd,mkt:br")
        return navegador

    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    async def conectando_pagina(self, navegador: webdriver.Chrome) -> None:
        await asyncio.sleep(1)
        element = navegador.find_element(By.XPATH, '//*[@id="yschsp"]')
        await asyncio.sleep(0.5)
        element.click()
        await asyncio.sleep(0.5)
        element.send_keys(self.acao)
        element.send_keys(Keys.RETURN)
        await asyncio.sleep(0.5)
        element_news = navegador.find_element(
            By.XPATH, '//*[@id="horizontal-bar"]/ol/li[1]/div/div/ul/li[4]/a'
        )
        await asyncio.sleep(1)
        element_news.click()

    async def beutfull_soup(
        self, navegador: webdriver.Chrome
    ) -> Optional[BeautifulSoup]:
        element_text = navegador.find_element(By.XPATH, '//*[@id="main"]')
        html = element_text.get_attribute("outerHTML")

        if html is not None:
            soup = BeautifulSoup(html, "html.parser")
            return soup
        else:
            print("Erro: não foi possível obter o HTML do elemento")
            return None

    async def get_text_async(self, element: Tag) -> str:
        return element.get_text()

    async def extract_link(self, article: Tag) -> Optional[str]:
        """Extract link from an article tag if it exists"""
        if isinstance(article, Tag):
            link = article.find("a")
            if link is not None and isinstance(link, Tag) and link.has_attr("href"):
                return link.get("href")  # type: ignore
        return None

    async def pegando_links(self, soup: BeautifulSoup) -> List[str]:
        # Use o método find_all para encontrar os elementos desejados
        news_articles = soup.find_all("div", class_="NewsArticle")

        # Process all articles concurrently using gather
        results = await asyncio.gather(
            *[self.extract_link(article) for article in news_articles]  # type: ignore
        )

        # Filter out None values
        dados_link = [link for link in results if link is not None]

        return dados_link

    async def pegando_titulo(self, soup: BeautifulSoup) -> List[str]:
        titulos = soup.find_all("h4", class_="s-title")
        dados_titulo = await asyncio.gather(
            # *[self.get_text_async(titulo) for titulo in titulos]
            *[
                self.get_text_async(titulo)
                for titulo in titulos
                if isinstance(titulo, Tag)
            ]
        )
        return dados_titulo  # type: ignore

    async def pegar_fonte(self, soup: BeautifulSoup) -> List[str]:
        fontes: List[Tag] = soup.find_all(class_="s-source mr-5 cite-co")  # type: ignore
        fonte_texto = await asyncio.gather(
            # *[self.get_text_async(fonte) for fonte in fontes]
            *[self.get_text_async(fonte) for fonte in fontes if isinstance(fonte, Tag)]
        )
        return list(fonte_texto)

    async def pegar_data(self, soup: BeautifulSoup) -> List[str]:
        tempos: List[Tag] = soup.find_all(class_="fc-2nd s-time mr-8")  # type: ignore
        tempo_texto = await asyncio.gather(
            # *[self.get_text_async(tempo) for tempo in tempos]
            *[self.get_text_async(tempo) for tempo in tempos if isinstance(tempo, Tag)]
        )
        return list(tempo_texto)

    async def pular_pagina(self, navegador: webdriver.Chrome, number: int) -> None:
        try:
            if number == 1:
                await self.sleep(1)
                element_proximo = navegador.find_element(
                    By.XPATH, '//*[@id="left"]/div/ol/li/div/div/a'
                )
                await self.sleep(1)
                element_proximo.click()
            else:
                await self.sleep(1)
                element_proximo = navegador.find_element(
                    By.XPATH, '//*[@id="left"]/div/ol/li/div/div/a[2]'
                )
                await self.sleep(1)
                element_proximo.click()
        except NoSuchElementException:
            print("Sem mais páginas!")

    async def selecionar_relevancia_tempo(
        self, navegador: webdriver.Chrome, tipo: str = "data"
    ) -> None:
        relevancia_tempo = navegador.find_element(
            By.XPATH, '//*[@id="horizontal-bar"]/ol/li[3]/div/div[2]/a'
        )
        relevancia_tempo.click()

        await self.sleep(1)

        elemento_atual = navegador.find_element(
            By.XPATH, "//*[@id='horizontal-bar']/ol/li[3]/div/div[2]/a/b"
        )
        await self.sleep(1)
        texto = elemento_atual.text

        texto_sem_acentuacao = unidecode.unidecode(texto).lower()

        if tipo == "data" and "data" not in texto_sem_acentuacao:
            relevancia_tempo = navegador.find_element(
                By.XPATH, '//*[@id="horizontal-bar"]/ol/li[3]/div/div[1]/ul/li[2]/a'
            )
            await self.sleep(1)
            relevancia_tempo.click()
        elif tipo == "relevancia" and "relevancia" not in texto_sem_acentuacao:
            relevancia_tempo = navegador.find_element(
                By.XPATH, '//*[@id="horizontal-bar"]/ol/li[3]/div/div[1]/ul/li[1]/a'
            )
            await self.sleep(1)
            relevancia_tempo.click()

    async def process_page(
        self, soup: BeautifulSoup, page_num: int, dict_dados: Dict[str, List[str]]
    ) -> None:
        """Process a single page of search results asynchronously"""
        links, titulos, fontes, datas = await asyncio.gather(
            self.pegando_links(soup),
            self.pegando_titulo(soup),
            self.pegar_fonte(soup),
            self.pegar_data(soup),
        )

        if links:
            dict_dados["links"].extend(links)
        else:
            print(f"Não foi possível pegar os links da pagina {page_num}!")

        if titulos:
            dict_dados["titulos"].extend(titulos)
        else:
            print(f"Não foi possível pegar os titulos da pagina {page_num}!")

        if fontes:
            dict_dados["fontes"].extend(fontes)
        else:
            print(f"Não foi possível pegar as fontes da pagina {page_num}!")

        if datas:
            dict_dados["datas"].extend(datas)
        else:
            print(f"Não foi possível pegar as datas da pagina {page_num}!")

    async def get_news(self, number_paginas: int) -> Dict[str, List[str]]:
        navegador = await self.navegador_get()
        await self.conectando_pagina(navegador)
        await self.selecionar_relevancia_tempo(navegador, self.tipo)
        await self.sleep(2)

        dict_dados: Dict[str, List[str]] = {
            "links": [],
            "titulos": [],
            "fontes": [],
            "datas": [],
        }

        for i in range(1, number_paginas + 1):
            soup = await self.beutfull_soup(navegador)

            if not soup:
                print(f"Erro ao obter o HTML da pagina {i}")
                break

            await self.process_page(soup, i, dict_dados)

            await self.pular_pagina(navegador, i)

        navegador.quit()
        return dict_dados
