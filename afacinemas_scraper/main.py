from typing import Dict, List

import requests_cache

from afacinemas_scraper.core.cinemas import ScraperCinemas
from afacinemas_scraper.core.lancamentos import ScraperLancamentos

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


if __name__ == "__main__":
    afa = Scraper()
    cinemas = afa.get_cinemas()
    proximos_lancamentos = afa.get_proximos_lancamentos()
    print(cinemas, "\n\n", proximos_lancamentos)
