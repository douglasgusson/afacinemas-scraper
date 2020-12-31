from typing import Dict, List

from bs4 import BeautifulSoup

from .base import ScraperBase


class ScraperLancamentos(ScraperBase):
    def __init__(self):
        super().__init__()
        self.url = self.base_url.format("breve.php")

    def _get_itens_novidades(self, soup: BeautifulSoup) -> List[BeautifulSoup]:
        return soup.find_all("div", {"class": "col-a-8 col-c-12"})

    def _get_titulo_novidade(self, soup: BeautifulSoup) -> str:
        return soup.find("div", {"style": "color:#494949"}).text

    def _get_estreia_novidade(self, soup: BeautifulSoup) -> str:
        texto = soup.find(
            "div",
            {"style": "color:#eb651a; text-align: justify; font-size: 13px"},
        ).text
        estreia = texto.split()[-1]
        return estreia

    def _get_descricao_novidade(self, soup: BeautifulSoup) -> str:
        descricao = soup.find(
            "div",
            {"style": "color:#494949; text-align: justify; font-size: 13px"},
        ).text
        return descricao

    def _get_classificacao_novidade(self, soup: BeautifulSoup) -> str:
        classificacao_el = soup.find_all(
            "div",
            {"style": "color:#494949; text-align: justify; font-size: 13px"},
        )[2]
        classificacao = classificacao_el.text.split(":")[-1].strip()
        return classificacao

    def _get_genero_novidade(self, soup: BeautifulSoup) -> str:
        genero_el = soup.find_all(
            "div",
            {"style": "color:#494949; text-align: justify; font-size: 13px"},
        )[3]
        genero = genero_el.text.split(":")[-1].strip()
        return genero

    def _get_duracao_novidade(self, soup: BeautifulSoup) -> str:
        duracao_el = soup.find_all(
            "div",
            {"style": "color:#494949; text-align: justify; font-size: 13px"},
        )[4]
        duracao = duracao_el.text.split(":")[-1].strip()
        return duracao

    def _get_src_poster_novidade(self, soup: BeautifulSoup) -> str:
        return self.base_url.format(soup.find("img")["src"])

    def extract(self) -> List[Dict]:
        try:
            soup = self._get_soup()
            itens = self._get_itens_novidades(soup)
            novidades = []

            for item in itens:
                novidade = {}
                novidade["titulo"] = self._get_titulo_novidade(item)
                novidade["estreia"] = self._get_estreia_novidade(item)
                novidade["poster"] = self._get_src_poster_novidade(item)
                novidade["descricao"] = self._get_descricao_novidade(item)
                novidade["classificacao"] = self._get_classificacao_novidade(
                    item
                )
                novidade["genero"] = self._get_genero_novidade(item)
                novidade["duracao"] = self._get_duracao_novidade(item)
                novidades.append(novidade)
            return novidades
        except TypeError:
            return []
