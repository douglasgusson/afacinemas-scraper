import os
from typing import Dict, List

from bs4 import BeautifulSoup

from .base import ScraperBase


class ScraperProgramacao(ScraperBase):
    def __init__(self):
        super().__init__()
        self.url = self.base_url.format("acess_painel.php?idc={}&dt={}")

    def _get_itens_programacao(
        self, soup: BeautifulSoup
    ) -> List[BeautifulSoup]:
        return soup.find_all("section", {"class": "colfilmes"})

    def _get_codigo_filme(self, soup: BeautifulSoup) -> str:
        return soup.find("button", {"class": "bsessao"})["property"]

    def _get_titulo_filme(self, soup: BeautifulSoup) -> str:
        return soup.find("h1").text

    def _get_url_capa(self, soup: BeautifulSoup) -> str:
        return soup.find("img", {"itemprop": "image"})["src"]

    def _get_classificacao(self, soup: BeautifulSoup) -> str:
        image_path = soup.find("img", {"class": "classificao"})["src"]
        classificacao = os.path.basename(image_path).split(".")[0]
        if classificacao.isdigit():
            return f"{classificacao} ANOS"
        return classificacao.upper()

    def _get_genero(self, soup: BeautifulSoup) -> str:
        return soup.find("p").text.split(" - ")[1].strip()

    def _get_duracao(self, soup: BeautifulSoup) -> str:
        return soup.find("p").text.split(" - ")[0].strip()

    def _get_sinopse(self, soup: BeautifulSoup) -> List[Dict]:
        return soup.find("p", {"class": "sinopse"}).text

    def _get_sessao(self, soup: BeautifulSoup) -> Dict:
        sessao = {}
        sessao_data = soup.text.split()
        sessao["sala"] = f"{sessao_data[0]} {sessao_data[1]}"
        sessao["horario"] = sessao_data[2]
        sessao["audio"] = sessao_data[4].split("/")[0]
        sessao["imagem"] = sessao_data[4].split("/")[1]

        return sessao

    def _get_sessoes(self, soup: BeautifulSoup) -> List[Dict]:
        sessoes = []
        div_sessoes = soup.find("div", {"class": "sessoesfilme"})
        bottoes_sessoes = div_sessoes.find_all("button")

        for botao in bottoes_sessoes:
            sessoes.append(self._get_sessao(botao))

        return sessoes

    def extract(self, id_cinema: int, data_programacao: str) -> List[Dict]:
        try:
            self.url = self.url.format(id_cinema, data_programacao)
            soup = self._get_soup()
            itens = self._get_itens_programacao(soup)
            programacoes = []

            for item in itens:
                programacao_filme = {}
                programacao_filme["codigo"] = self._get_codigo_filme(item)
                programacao_filme["titulo"] = self._get_titulo_filme(item)
                programacao_filme["url_capa"] = self.base_url.format(
                    self._get_url_capa(item)
                )
                programacao_filme["classificacao"] = self._get_classificacao(
                    item
                )
                programacao_filme["genero"] = self._get_genero(item)
                programacao_filme["duracao"] = self._get_duracao(item)
                programacao_filme["sinopse"] = self._get_sinopse(item)
                programacao_filme["sessoes"] = self._get_sessoes(item)

                programacoes.append(programacao_filme)

            return programacoes
        except TypeError:
            return []
