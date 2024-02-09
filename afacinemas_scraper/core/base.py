import requests
from bs4 import BeautifulSoup


class ScraperBase:
    def __init__(self, proxies: dict = None):
        self.base_url = "https://afacinemas.com.br/{}"
        self.headers = {"User-agent": "Mozilla/5.0"}
        self.proxies = proxies

    def _get_soup(self) -> BeautifulSoup:
        req = requests.get(
            self.url,
            headers=self.headers,
            proxies=self.proxies,
        )
        if req.ok and req.status_code == 200:
            return BeautifulSoup(req.text, "html.parser")

    def extract(self):
        raise NotImplementedError("Please Implement this method")
