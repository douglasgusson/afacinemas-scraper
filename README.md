# Afa Cinemas Scraper 🦀

> **afacinemas-scraper** - Ferramenta para raspagem de dados do site da rede [Afa Cinemas](http://afacinemas.com.br/).

[![GitHub license](https://img.shields.io/github/license/douglasgusson/afacinemas-scraper)](https://github.com/douglasgusson/afacinemas-scraper/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/douglasgusson/afacinemas-scraper)](https://github.com/douglasgusson/afacinemas-scraper/issues)
[![GitHub forks](https://img.shields.io/github/forks/douglasgusson/afacinemas-scraper)](https://github.com/douglasgusson/afacinemas-scraper/network)
[![GitHub stars](https://img.shields.io/github/stars/douglasgusson/afacinemas-scraper)](https://github.com/douglasgusson/afacinemas-scraper/stargazers)

## ⚙️ Instalação

```sh
pip install afacinemas-scraper
```

## 💻 Utilização 

```python
from afacinemas_scraper import Scraper

scraper = Scraper()
```

### 🔍 Buscando os cinemas 

```python
from afacinemas_scraper import Scraper

scraper = Scraper()
cinemas = scraper.get_cinemas()

print(cinemas)
```

📄 Saída:
```python
[{'codigo': 4, 'nome': 'Boituva Cine Park', 'logo': 'http://afacinemas.com.br/logotipo/boituva.jpg', 'endereco': 'Avenida Vereador José Biagione, 660 Centro - Boituva /SP', 'contato': '(15) 3363-8083'}, ...]
```

### 🔍 Buscando os próximos lançamentos

```python
from afacinemas_scraper import Scraper

scraper = Scraper()

proximos_lancamentos = scraper.get_proximos_lancamentos()
print(proximos_lancamentos)
```

📄 Saída:
```python
[{'titulo': 'MONSTER HUNTER', 'estreia': '14/01/2021', 'poster': 'http://afacinemas.com.br/adm/cartazSite/hunter.jpg', 'descricao': 'Baseado no jogo da Capcom chamado Monster Hunter, a tenente Artemis e seus soldados são transportados para um novo mundo. Lá, eles se envolvem em batalhas imponentes, buscando desesperadamente a sobrevivência contra bestas gigantes portadoras de habilidades surreais.', 'classificacao': '14 ANOS', 'genero': 'AÇÃO', 'duracao': '110min'}, ...]
```

### 🔍 Buscando os preços dos ingressos

```python
from afacinemas_scraper import Scraper

scraper = Scraper()

precos_ingressos = afa.get_precos_ingressos(10)  # código do cinema
print(precos_ingressos)
```

📄 Saída:
```python
[{'dia_semana': 'Domingo', 'precos': [{'descricao': 'Inteira 2D', 'valor': 24.0}, {'descricao': 'Meia 2D', 'valor': 12.0}, {'descricao': 'Inteira 3D', 'valor': 24.0}, {'descricao': 'Meia 3D', 'valor': 12.0}]}, ...]
```
