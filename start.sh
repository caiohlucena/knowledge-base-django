#!/bin/bash
set -e

# Aplicar migrações
python manage.py migrate --noinput

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Iniciar servidor
gunicorn knowledge.wsgi:application --bind 0.0.0.0:$PORT
