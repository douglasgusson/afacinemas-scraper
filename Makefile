test:
	@pytest --cov=./afacinemas_scraper --cov-report=xml

black:
	@poetry run black . -l 80 --exclude=.venv

flake8:
	@poetry run flake8 --ignore=E501,W501,E231,W503

check: black flake8

format:
	@black -l 80 . --exclude=.venv

install:
	@poetry install
	@pre-commit install

sh:
	@poetry shell

.PHONY: test format check install sh
