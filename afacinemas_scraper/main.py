from typing import Dict, List

import requests_cache

from afacinemas_scraper.core.cinemas import ScraperCinemas
from afacinemas_scraper.core.lancamentos import ScraperLancamentos
from afacinemas_scraper.core.precos import ScraperPrecos
from afacinemas_scraper.core.programacao import ScraperProgramacao

requests_cache.install_cache(
    "cache_afacinemas", backend="sqlite", expire_after=600
)


class Scraper:
    def __init__(self, proxies: dict = None, headers: dict = None):
        self.proxies = proxies
        self.headers = headers

    def get_cinemas(self) -> List[Dict]:
        sc = ScraperCinemas(proxies=self.proxies, headers=self.headers)
        return sc.extract()

    def get_proximos_lancamentos(self) -> List[Dict]:
        sc = ScraperLancamentos(proxies=self.proxies, headers=self.headers)
        return sc.extract()

    def get_precos_ingressos(self, codigo: int):
        sc = ScraperPrecos(proxies=self.proxies, headers=self.headers)
        return sc.extract(codigo)

    def get_programacao(self, codigo: int, data: str):
        sc = ScraperProgramacao(proxies=self.proxies, headers=self.headers)
        return sc.extract(codigo, data)


if __name__ == "__main__":
    afa = Scraper(proxies={})
    lancamentos = afa.get_proximos_lancamentos()
    print(len(lancamentos), lancamentos)
