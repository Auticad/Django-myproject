# MyProject — Django 5.2 LTS Full-Stack

[![Django CI/CD](https://github.com/TUO-USERNAME/myproject/actions/workflows/ci.yml/badge.svg)](https://github.com/TUO-USERNAME/myproject/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Django 5.2](https://img.shields.io/badge/django-5.2%20LTS-green.svg)](https://docs.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Progetto Django 5.2 LTS full-stack con ORM, DRF, autenticazione JWT, Celery, Docker e deploy completo.

---

## Stack tecnologico

| Componente     | Tecnologia                  |
|----------------|-----------------------------|
| Framework      | Django 5.2 LTS              |
| Database       | PostgreSQL 16               |
| Cache / Broker | Redis 7                     |
| Task queue     | Celery 5 + django-celery-beat |
| REST API       | Django REST Framework + SimpleJWT |
| Frontend       | Django Templates + Bootstrap 5 + HTMX |
| WSGI Server    | Gunicorn                    |
| Reverse proxy  | Nginx                       |
| Container      | Docker + Docker Compose     |
| CI/CD          | GitHub Actions              |
| Monitoring     | Sentry                      |

---

## Avvio rapido (sviluppo locale)

### 1. Clona il repository

```bash
git clone https://github.com/TUO-USERNAME/myproject.git
cd myproject
```

### 2. Crea e attiva il virtualenv

```bash
# Con uv (raccomandato)
uv venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate          # Windows

# Con venv standard
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Installa le dipendenze

```bash
pip install -r requirements-dev.txt
# oppure con uv:
uv pip install -r requirements-dev.txt
```

### 4. Configura le variabili d'ambiente

```bash
cp .env.example .env
# Modifica .env con i tuoi valori (vedi sezione Configurazione)
```

### 5. Avvia PostgreSQL e Redis

```bash
# Con Docker (modo più semplice per sviluppo)
docker run -d --name pg -e POSTGRES_DB=myproject_db \
  -e POSTGRES_USER=myproject_user -e POSTGRES_PASSWORD=password_locale \
  -p 5432:5432 postgres:16-alpine

docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### 6. Esegui le migrazioni e crea il superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Avvia il server

```bash
python manage.py runserver
# oppure
make dev
```

Apri [http://localhost:8000](http://localhost:8000) nel browser.  
Admin disponibile su [http://localhost:8000/admin/](http://localhost:8000/admin/).  
Docs API su [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/).

---

## Avvio con Docker Compose (stack completo)

```bash
# Copia e configura .env
cp .env.example .env

# Avvia tutti i servizi (web, db, redis, celery, nginx)
docker-compose up --build -d

# Verifica i log
docker-compose logs -f web

# Esegui le migrazioni
docker-compose exec web python manage.py migrate

# Crea il superuser
docker-compose exec web python manage.py createsuperuser
```

---

## Configurazione (.env)

Copia `.env.example` in `.env` e compila i valori:

```env
SECRET_KEY=<genera con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=myproject_db
DB_USER=myproject_user
DB_PASSWORD=password_locale
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tua@email.com
EMAIL_HOST_PASSWORD=app_password

SENTRY_DSN=   # lascia vuoto in sviluppo
```

---

## Comandi utili (Makefile)

```bash
make help         # lista tutti i comandi
make dev          # avvia server di sviluppo
make migrate      # applica migrazioni
make migrations   # crea nuove migrazioni
make test         # esegui test con coverage
make superuser    # crea superuser
make shell        # Django shell
make docker-up    # avvia stack Docker
make docker-down  # ferma stack Docker
make clean        # rimuovi file temporanei
```

---

## Test

```bash
# Tutti i test
pytest

# Con coverage HTML
pytest --cov=apps --cov-report=html
open htmlcov/index.html

# Test rapidi (escludi slow)
pytest -m "not slow"
```

---

## Struttura del progetto

```
myproject/
├── config/               # Configurazione Django
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   ├── middleware.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/            # App utenti (CustomUser)
│   ├── blog/             # App blog (Post, Category, Tag)
│   └── api/              # DRF API (serializers, viewsets)
├── templates/            # Template HTML globali
├── static/               # File statici
├── media/                # Upload utenti (non in git)
├── tests/                # Test pytest
├── docker/               # Dockerfile, nginx.conf, gunicorn.conf.py
├── .github/workflows/    # GitHub Actions CI/CD
├── docker-compose.yml
├── docker-compose.dev.yml
├── Makefile
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

---

## API Endpoints principali

| Metodo | Endpoint                      | Descrizione              | Auth |
|--------|-------------------------------|--------------------------|------|
| GET    | `/api/posts/`                 | Lista post pubblicati    | No   |
| POST   | `/api/posts/`                 | Crea nuovo post          | Sì   |
| GET    | `/api/posts/{slug}/`          | Dettaglio post           | No   |
| PUT    | `/api/posts/{slug}/`          | Aggiorna post            | Sì   |
| DELETE | `/api/posts/{slug}/`          | Elimina post             | Sì   |
| GET    | `/api/posts/{slug}/related/`  | Post correlati           | No   |
| GET    | `/api/categories/`            | Lista categorie          | No   |
| GET    | `/api/tags/`                  | Lista tag                | No   |
| POST   | `/api/auth/token/`            | Ottieni JWT              | No   |
| POST   | `/api/auth/token/refresh/`    | Rinnova access token     | No   |
| GET    | `/api/docs/`                  | Swagger UI               | No   |

---

## Deploy produzione

Vedi [docs/deploy.md](docs/deploy.md) per la guida completa al deploy su VPS con Nginx, SSL e GitHub Actions.

---

## Licenza

MIT — vedi [LICENSE](LICENSE)
