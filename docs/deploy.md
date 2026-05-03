# Guida al Deploy su VPS

Guida completa per deployare MyProject su un VPS Ubuntu 22.04 / 24.04
con Docker, Nginx e SSL Let's Encrypt.

---

## Prerequisiti

- VPS con Ubuntu 22.04+ (min 2 vCPU, 2 GB RAM)
- Dominio configurato con record A puntato all'IP del VPS
- Accesso SSH come root o utente con sudo

---

## 1. Preparazione del server

```bash
# Aggiorna il sistema
apt update && apt upgrade -y

# Installa tool base
apt install -y git curl wget ufw fail2ban

# Configura firewall
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# Crea utente deploy (non usare root)
adduser deploy
usermod -aG sudo deploy
# Copia la chiave SSH
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

---

## 2. Installa Docker

```bash
# Installa Docker ufficiale
curl -fsSL https://get.docker.com | sh
usermod -aG docker deploy

# Installa Docker Compose plugin
apt install -y docker-compose-plugin
docker compose version   # verifica
```

---

## 3. Clona il repository

```bash
su - deploy
git clone git@github.com:TUO-USERNAME/myproject.git /app
cd /app
```

---

## 4. Configura le variabili d'ambiente

```bash
cp .env.example .env
nano .env
```

Valori minimi da impostare per produzione:

```env
SECRET_KEY=<chiave-lunga-e-casuale>
DEBUG=False
ALLOWED_HOSTS=mysite.com,www.mysite.com
ENVIRONMENT=production

DB_NAME=myproject_db
DB_USER=myproject_user
DB_PASSWORD=<password-sicura>
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/0

EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.xxxxx

SENTRY_DSN=https://xxx@sentry.io/project_id
```

Genera la SECRET_KEY con:

```bash
python3 -c "from secrets import token_urlsafe; print(token_urlsafe(50))"
```

---

## 5. Configura Nginx con il tuo dominio

```bash
nano docker/nginx.conf
# Sostituisci "mysite.com" con il tuo dominio reale
```

---

## 6. Primo avvio senza SSL (per Certbot)

Modifica temporaneamente `docker/nginx.conf` per usare solo HTTP:

```nginx
server {
    listen 80;
    server_name mysite.com www.mysite.com;
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 200 'ok'; }
}
```

Avvia solo Nginx e db:

```bash
docker compose up -d db redis nginx
```

---

## 7. Ottieni il certificato SSL

```bash
docker run --rm \
  -v /app/certbot_conf:/etc/letsencrypt \
  -v /app/certbot_www:/var/www/certbot \
  certbot/certbot certonly --webroot \
  -w /var/www/certbot \
  -d mysite.com -d www.mysite.com \
  --email tua@email.com \
  --agree-tos --non-interactive
```

---

## 8. Avvio completo

Ripristina il `nginx.conf` originale con SSL, poi:

```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

---

## 9. Verifica

```bash
# Stato servizi
docker compose ps

# Log web
docker compose logs -f web

# Health check
curl https://mysite.com/health/

# Sicurezza Django
docker compose exec web python manage.py check --deploy
```

---

## 10. Rinnovo automatico SSL

Aggiungi un crontab per il rinnovo automatico:

```bash
crontab -e
# Aggiungi questa riga:
0 3 * * * cd /app && docker run --rm -v /app/certbot_conf:/etc/letsencrypt -v /app/certbot_www:/var/www/certbot certbot/certbot renew --quiet && docker compose exec nginx nginx -s reload
```

---

## 11. Aggiornamenti (deploy manuale)

```bash
cd /app
git pull origin main
docker compose up --build -d --no-deps web celery celery-beat
docker compose exec -T web python manage.py migrate --noinput
docker image prune -f
```

Con GitHub Actions il deploy è automatico al push su `main`
(richiede i secret `SERVER_HOST`, `SERVER_USER`, `SSH_PRIVATE_KEY`).

---

## Secret GitHub Actions da configurare

Vai su **GitHub → Repository → Settings → Secrets and variables → Actions**:

| Secret           | Valore                             |
|------------------|------------------------------------|
| `SERVER_HOST`    | IP o hostname del VPS              |
| `SERVER_USER`    | `deploy`                           |
| `SSH_PRIVATE_KEY`| Chiave privata SSH (contenuto file)|
| `SERVER_PORT`    | `22` (opzionale)                   |

---

## Checklist finale produzione

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` diversa da sviluppo
- [ ] `ALLOWED_HOSTS` con dominio reale
- [ ] Certificato SSL attivo
- [ ] `python manage.py check --deploy` senza errori
- [ ] Backup automatico PostgreSQL configurato
- [ ] Sentry DSN configurato
- [ ] Rate limiting Nginx attivo
- [ ] Rinnovo SSL automatico testato
