from typing import Dict, List

from bs4 import BeautifulSoup

from .base import ScraperBase


class ScraperCinemas(ScraperBase):
    def __init__(self):
        super().__init__()
        self.url = self.base_url.format("cinemas.php")

    def _get_itens_cinemas(self, soup: BeautifulSoup) -> List[BeautifulSoup]:
        return soup.find_all("section", {"class": "cartazbreve"})

    def _get_codigo_cinema(self, soup: BeautifulSoup) -> int:
        codigo = int(soup.attrs.get("property"))
        return codigo

    def _get_nome_cinema(self, soup: BeautifulSoup) -> str:
        nome = soup.attrs.get("title")
        return nome

    def _get_src_logo_cinema(self, soup: BeautifulSoup) -> str:
        return self.base_url.format(soup.find("img").get("src"))

    def _get_cidade_cinema(self, soup: BeautifulSoup) -> str:
        section_databreve = soup.find("section", {"class": "databreve"})
        p_cidade = section_databreve("p")[-1]
        return p_cidade.text.strip()

    def extract(self) -> List[Dict]:
        try:
            soup = self._get_soup()
            itens = self._get_itens_cinemas(soup)
            cinemas = []

            for item in itens:
                cinema = {}
                cinema["codigo"] = self._get_codigo_cinema(item)
                cinema["nome"] = self._get_nome_cinema(item)
                cinema["url_logo"] = self._get_src_logo_cinema(item)
                cinema["cidade"] = self._get_cidade_cinema(item)
                cinemas.append(cinema)
            return cinemas
        except TypeError:
            return []
