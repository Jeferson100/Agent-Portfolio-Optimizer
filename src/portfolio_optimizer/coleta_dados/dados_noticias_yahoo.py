import time
import warnings
from typing import Any, Dict, List

import unidecode
from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv
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

load_dotenv()


class DadosNoticiasBuscadorYahoo:
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

    def navegador_get(self) -> webdriver.Chrome:
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

    def conectando_pagina(self, navegador: webdriver.Chrome) -> None:
        time.sleep(2)
        element = navegador.find_element(By.XPATH, '//*[@id="yschsp"]')
        time.sleep(1)
        element.click()
        time.sleep(1)
        element.send_keys(self.acao)
        element.send_keys(Keys.RETURN)
        time.sleep(1)
        element_news = navegador.find_element(
            By.XPATH, '//*[@id="horizontal-bar"]/ol/li[1]/div/div/ul/li[4]/a'
        )
        time.sleep(1)
        element_news.click()

    def beutfull_soup(self, navegador: webdriver.Chrome) -> BeautifulSoup | None:
        element_text = navegador.find_element(By.XPATH, '//*[@id="main"]')

        html = element_text.get_attribute("outerHTML")

        if html is not None:
            soup = BeautifulSoup(html, "html.parser")
            return soup
        else:
            print("Erro: não foi possível obter o HTML do elemento")
            return None

    def pegando_links(self, soup: BeautifulSoup) -> List[Any]:
        # Use o método find_all para encontrar os elementos desejados
        news_articles = soup.find_all("div", class_="NewsArticle")

        dados_link = []
        for article in news_articles:
            if isinstance(article, Tag):
                link = article.find("a")
                if link is not None and isinstance(link, Tag) and link.has_attr("href"):
                    dados_link.append(link.get("href"))
        return dados_link

    def pegando_titulo(self, soup: BeautifulSoup) -> List[str]:
        titulos = soup.find_all("h4", class_="s-title")

        # Extraia os textos dos títulos
        dados_titulo = [titulo.get_text() for titulo in titulos]

        return dados_titulo

    def pegar_fonte(self, soup: BeautifulSoup) -> List[str]:
        fontes = soup.find_all(class_="s-source mr-5 cite-co")

        fonte_texto = [fonte.get_text() for fonte in fontes]

        return fonte_texto

    def pegar_data(self, soup: BeautifulSoup) -> List[str]:
        tempos = soup.find_all(class_="fc-2nd s-time mr-8")

        tempo_texto = [tempo.get_text() for tempo in tempos]

        return tempo_texto

    def pular_pagina(self, navegador: webdriver.Chrome, number: int) -> None:
        try:
            if number == 1:
                time.sleep(1)
                element_proximo = navegador.find_element(
                    By.XPATH, '//*[@id="left"]/div/ol/li/div/div/a'
                )
                time.sleep(1)
                element_proximo.click()
            else:
                time.sleep(1)
                element_proximo = navegador.find_element(
                    By.XPATH, '//*[@id="left"]/div/ol/li/div/div/a[2]'
                )
                time.sleep(1)
                element_proximo.click()
        except NoSuchElementException:
            print("Sem mais páginas!")

    def selecionar_relevancia_tempo(
        self, navegador: webdriver.Chrome, tipo: str = "data"
    ) -> None:
        relevancia_tempo = navegador.find_element(
            By.XPATH, '//*[@id="horizontal-bar"]/ol/li[3]/div/div[2]/a'
        )
        relevancia_tempo.click()

        time.sleep(1)

        elemento_atual = navegador.find_element(
            By.XPATH, "//*[@id='horizontal-bar']/ol/li[3]/div/div[2]/a/b"
        )
        time.sleep(1)
        texto = elemento_atual.text

        texto_sem_acentuacao = unidecode.unidecode(texto).lower()

        if tipo == "data" and "data" not in texto_sem_acentuacao:
            relevancia_tempo = navegador.find_element(
                By.XPATH, '//*[@id="horizontal-bar"]/ol/li[3]/div/div[1]/ul/li[2]/a'
            )
            time.sleep(1)
            relevancia_tempo.click()
        elif tipo == "relevancia" and "relevancia" not in texto_sem_acentuacao:
            relevancia_tempo = navegador.find_element(
                By.XPATH, '//*[@id="horizontal-bar"]/ol/li[3]/div/div[1]/ul/li[1]/a'
            )
            time.sleep(1)
            relevancia_tempo.click()

    def get_news_link(self, number_paginas: int) -> List[str]:
        navegador = self.navegador_get()
        self.conectando_pagina(navegador)
        self.selecionar_relevancia_tempo(navegador, self.tipo)
        time.sleep(2)
        links: List[str] = []
        for i in range(1, number_paginas + 1):
            soup = self.beutfull_soup(navegador)
            if not soup:
                print(f"Erro ao obter o HTML da pagina {i}")
                break
            links.extend(self.pegando_links(soup))

            self.pular_pagina(navegador, i)

        return links

    def get_news(self, number_paginas: int) -> Dict[str, List[str]]:
        navegador = self.navegador_get()
        self.conectando_pagina(navegador)
        self.selecionar_relevancia_tempo(navegador, self.tipo)
        time.sleep(2)
        dict_dados: Dict[str, List[str]] = {}
        dict_dados["links"] = []
        dict_dados["titulos"] = []
        dict_dados["fontes"] = []
        dict_dados["datas"] = []
        for i in range(1, number_paginas + 1):
            soup = self.beutfull_soup(navegador)

            if not soup:
                print(f"Erro ao obter o HTML da pagina {i}")
                break
            links = self.pegando_links(soup)
            if links:
                dict_dados["links"].extend(links)
            else:
                print(f"Não foi possível pegar os links da pagina {i}!")

            titulos = self.pegando_titulo(soup)
            if titulos:
                dict_dados["titulos"].extend(titulos)
            else:
                print(f"Não foi possível pegar os titulos da pagina {i}!")

            fontes = self.pegar_fonte(soup)
            if fontes:
                dict_dados["fontes"].extend(fontes)
            else:
                print(f"Não foi possível pegar as fontes da pagina {i}!")

            datas = self.pegar_data(soup)
            if datas:
                dict_dados["datas"].extend(datas)
            else:
                print(f"Não foi possível pegar as datas da pagina {i}!")

            self.pular_pagina(navegador, i)

        return dict_dados
