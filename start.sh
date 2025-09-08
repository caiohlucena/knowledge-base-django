#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn dicionario_financeiro.wsgi:application --bind 0.0.0.0:$PORT
