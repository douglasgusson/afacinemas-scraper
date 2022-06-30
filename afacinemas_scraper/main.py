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
    def get_cinemas(self) -> List[Dict]:
        sc = ScraperCinemas()
        return sc.extract()

    def get_proximos_lancamentos(self) -> List[Dict]:
        sc = ScraperLancamentos()
        return sc.extract()

    def get_precos_ingressos(self, codigo: int):
        sc = ScraperPrecos()
        return sc.extract(codigo)

    def get_programacao(self, codigo: int, data: str):
        sc = ScraperProgramacao()
        return sc.extract(codigo, data)


if __name__ == "__main__":
    afa = Scraper()
    programacao = afa.get_programacao(10, "2022-06-30")
    print(programacao)
