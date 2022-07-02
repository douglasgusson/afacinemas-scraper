from typing import Dict, List

from bs4 import BeautifulSoup

from afacinemas_scraper.core.filme import ScraperFilme

from .base import ScraperBase


class ScraperLancamentos(ScraperBase):
    def __init__(self):
        super().__init__()
        self.url = self.base_url.format("breve_filmes.php")

    def _get_itens_novidades(self, soup: BeautifulSoup) -> List[BeautifulSoup]:
        return soup.find_all("section", {"class": "cartazbreve"})

    def _get_codigo_filme(self, soup: BeautifulSoup) -> int:
        return int(soup.attrs["property"])

    def extract(self) -> List[Dict]:
        try:
            soup = self._get_soup()
            itens = self._get_itens_novidades(soup)
            novidades = []

            for item in itens:
                codigo = self._get_codigo_filme(item)
                sf = ScraperFilme()
                filme = sf.extract(codigo)

                novidade = {}
                novidade["codigo"] = codigo
                novidade["titulo"] = filme.get("titulo")
                novidade["estreia"] = filme.get("estreia")
                novidade["poster"] = filme.get("url_capa")
                novidade["descricao"] = filme.get("sinopse")
                novidade["classificacao"] = filme.get("classificacao")
                novidade["duracao"] = filme.get("duracao")

                novidades.append(novidade)
            return novidades
        except TypeError:
            return []
