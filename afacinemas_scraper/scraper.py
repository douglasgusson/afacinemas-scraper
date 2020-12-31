from typing import Dict, List

import requests
import requests_cache
from bs4 import BeautifulSoup

requests_cache.install_cache(
    "cache_afacinemas", backend="sqlite", expire_after=600
)


class ScraperBase:
    def __init__(self):
        self.base_url = "http://afacinemas.com.br/{}"

    def _get_soup(self) -> BeautifulSoup:
        req = requests.get(self.url)
        if req.ok and req.status_code == 200:
            return BeautifulSoup(req.text, "html.parser")

    def extract(self):
        raise NotImplementedError("Please Implement this method")


class ScraperCinemas(ScraperBase):
    def __init__(self):
        super().__init__()
        self.url = self.base_url.format("cinemas.php")

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


class ScraperNovidades(ScraperBase):
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


class Scraper:
    def get_cinemas(self) -> List[Dict]:
        sc = ScraperCinemas()
        return sc.extract()

    def get_proximos_lancamentos(self) -> List[Dict]:
        sc = ScraperNovidades()
        return sc.extract()


if __name__ == "__main__":
    afa = Scraper()
    cinemas = afa.get_cinemas()
    proximos_lancamentos = afa.get_proximos_lancamentos()
    print(cinemas, "\n\n", proximos_lancamentos)
