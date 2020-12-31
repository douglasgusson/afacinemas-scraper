# Afa Cinemas Scraper 🦀
Ferramenta para raspagem de dados do site da rede [Afa Cinemas](http://afacinemas.com.br/).

## Instalação

```sh
pip install afacinemas-scraper
```

## Uso 

```python
from afacinemas_scraper import Scraper

scraper = Scraper()
```

### Buscando os cinemas 

```python
from afacinemas_scraper import Scraper

scraper = Scraper()
cinemas = scraper.get_cinemas()

print(cinemas)
```

### Buscando os próximos lançamentos

```python
from afacinemas_scraper import Scraper

scraper = Scraper()

proximos_lancamentos = scraper.get_proximos_lancamentos()
print(proximos_lancamentos)
```