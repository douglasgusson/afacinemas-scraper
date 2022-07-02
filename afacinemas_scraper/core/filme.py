import os
from typing import Dict

from bs4 import BeautifulSoup

from .base import ScraperBase


class ScraperFilme(ScraperBase):
    def __init__(self):
        super().__init__()
        self.url = self.base_url.format("filmes.php?idf={}")

    def _get_elemento_filme(self, soup: BeautifulSoup) -> BeautifulSoup:
        return soup.find("section", {"class": "boxbrevefilme"})

    def _get_capa_filme(self, soup: BeautifulSoup) -> str:
        return soup.find("img").attrs["src"]

    def _get_titulo_filme(self, soup: BeautifulSoup) -> str:
        return soup.find("h1").text

    def _get_estreia_filme(self, soup: BeautifulSoup) -> str:
        return soup.find("section", {"class": "databreve"}).text.strip()

    def _get_sinopse_filme(self, soup: BeautifulSoup) -> str:
        session_dados_filme = soup.find("section", {"class": "brevedadosfilme"})
        p_sinopse = session_dados_filme("p")[1]
        sinopse = " ".join(p_sinopse.text.split())
        return sinopse

    def _get_classificacao_filme(self, soup: BeautifulSoup) -> str:
        image_path = soup.find("img", {"class": "classificao"})["src"]
        classificacao = os.path.basename(image_path).split(".")[0]
        if classificacao.isdigit():
            return f"{classificacao} ANOS"
        return classificacao.upper()

    def _get_duracao_filme(self, soup: BeautifulSoup) -> str:
        session_dados_filme = soup.find("section", {"class": "brevedadosfilme"})
        return session_dados_filme.find("p").text.strip()

    def extract(self, id_filme: int) -> Dict:
        try:
            self.url = self.url.format(id_filme)
            soup = self._get_soup()
            soup_filme = self._get_elemento_filme(soup)

            filme = {}
            filme["codigo"] = id_filme
            filme["url_capa"] = self.base_url.format(
                self._get_capa_filme(soup_filme)
            )
            filme["titulo"] = self._get_titulo_filme(soup_filme)
            filme["estreia"] = self._get_estreia_filme(soup_filme)
            filme["sinopse"] = self._get_sinopse_filme(soup_filme)
            filme["classificacao"] = self._get_classificacao_filme(soup_filme)
            filme["duracao"] = self._get_duracao_filme(soup_filme)

            return filme
        except TypeError:
            return {}
