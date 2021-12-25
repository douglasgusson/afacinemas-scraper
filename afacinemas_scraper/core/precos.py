from typing import Dict, List

from bs4 import BeautifulSoup

from .base import ScraperBase


class ScraperPrecos(ScraperBase):
    def __init__(self):
        super().__init__()
        self.url = self.base_url.format("preco2.php?idp={}")

    def _get_itens_precos(self, soup: BeautifulSoup) -> List[BeautifulSoup]:
        return soup.find_all("div", {"class": "col-a-15 col-b-4 col-c-12"})

    def _get_dia_semana_preco(self, soup: BeautifulSoup) -> int:
        return soup.find("div").text

    def _get_precos(self, soup: BeautifulSoup) -> List[Dict]:
        elementos = soup.find_all("div", {"class": "col-a-12"})
        precos = []
        for el in elementos[1:5]:
            preco = self._get_preco(el)
            if preco:
                precos.append(preco)
        return precos

    def _get_preco(self, soup: BeautifulSoup) -> Dict:
        descricao = soup.find("div", {"class": "col-a-8"})
        valor = soup.find("div", {"class": "col-a-4"})

        if descricao and valor:
            return {"descricao": descricao.text, "valor": float(valor.text)}

    def extract(self, id_cinema: int) -> List[Dict]:
        try:
            self.url = self.url.format(id_cinema)
            soup = self._get_soup()
            itens = self._get_itens_precos(soup)
            precos = []

            for item in itens:
                tabela = {}
                tabela["dia_semana"] = self._get_dia_semana_preco(item)
                tabela["precos"] = self._get_precos(item)
                precos.append(tabela)

            # Preços de feriado igual aos de domingo
            precos.append(
                {"dia_semana": "Feriado", "precos": precos[0]["precos"]}
            )
            return precos
        except TypeError:
            return []
