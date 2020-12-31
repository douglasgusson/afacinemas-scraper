from typing import Dict, List

import requests
import requests_cache
from bs4 import BeautifulSoup

requests_cache.install_cache(
    "cache_afacinemas", backend="sqlite", expire_after=600
)


class ScraperCinemas:
    def __init__(self):
        self.base_url = "http://afacinemas.com.br/{}"
        self.url_cinemas = self.base_url.format("cinemas.php")

    def _get_soup(self) -> BeautifulSoup:
        req = requests.get(self.url_cinemas)
        if req.ok and req.status_code == 200:
            return BeautifulSoup(req.text, "html.parser")

    def _get_itens_cinemas(self, soup: BeautifulSoup) -> List[BeautifulSoup]:
        return soup.find_all("div", {"class": "col-a-6 col-c-12"})

    def _get_codigo_cinema(self, soup: BeautifulSoup) -> int:
        a = soup.find_all("a")[-1]
        codigo = int(a["href"].split("'")[-2].split("=")[-1])
        return codigo

    def _get_nome_cinema(self, soup: BeautifulSoup) -> str:
        return soup.find("div", {"style": "color:#494949"}).text

    def _get_src_logo_cinema(self, soup: BeautifulSoup) -> str:
        return self.base_url.format(soup.find("img")["src"])

    def _get_endereco_cinema(self, soup: BeautifulSoup) -> str:
        endereco_itens = soup.find_all(
            "div",
            {"style": "color:#494949; text-align: justify; font-size: 13px"},
        )
        textos = [item.text for item in endereco_itens]
        return " ".join(textos)

    def _get_contato_cinema(self, soup: BeautifulSoup) -> str:
        return soup.find(
            "div",
            {"style": "color:#eb651a; text-align: justify; font-size: 13px"},
        ).text

    def extract(self) -> List[Dict]:
        try:
            soup = self._get_soup()
            itens = self._get_itens_cinemas(soup)
            cinemas = []

            for item in itens:
                cinema = {}
                cinema["codigo"] = self._get_codigo_cinema(item)
                cinema["nome"] = self._get_nome_cinema(item)
                cinema["logo"] = self._get_src_logo_cinema(item)
                cinema["endereco"] = self._get_endereco_cinema(item)
                cinema["contato"] = self._get_contato_cinema(item)
                cinemas.append(cinema)
            return cinemas
        except TypeError:
            return []


class Scraper:
    def get_cinemas(self) -> List[Dict]:
        sc = ScraperCinemas()
        return sc.extract()


if __name__ == "__main__":
    afa = Scraper()
    cinemas = afa.get_cinemas()
    print(cinemas)
