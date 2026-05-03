# Makefile — comandi abbreviati per MyProject
.PHONY: help install dev run migrate test lint clean docker-up docker-down

PYTHON   = python
MANAGE   = $(PYTHON) manage.py
DC       = docker-compose

help:
	@echo "Comandi disponibili:"
	@echo "  make install     — installa dipendenze"
	@echo "  make dev         — avvia server di sviluppo"
	@echo "  make migrate     — esegui migrazioni"
	@echo "  make migrations  — crea nuove migrazioni"
	@echo "  make test        — esegui test con coverage"
	@echo "  make superuser   — crea superuser"
	@echo "  make shell       — apri shell Django"
	@echo "  make docker-up   — avvia stack Docker"
	@echo "  make docker-down — ferma stack Docker"
	@echo "  make clean       — rimuovi file temporanei"

install:
	pip install -r requirements-dev.txt

dev:
	$(MANAGE) runserver

migrate:
	$(MANAGE) migrate

migrations:
	$(MANAGE) makemigrations

test:
	pytest --cov=apps --cov-report=html --cov-report=term-missing

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

static:
	$(MANAGE) collectstatic --noinput

check:
	$(MANAGE) check --deploy

docker-up:
	$(DC) up --build -d

docker-down:
	$(DC) down

docker-logs:
	$(DC) logs -f web

docker-shell:
	$(DC) exec web $(MANAGE) shell

docker-migrate:
	$(DC) exec web $(MANAGE) migrate

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	rm -rf htmlcov/ .coverage coverage.xml
