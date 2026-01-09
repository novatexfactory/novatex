#!/bin/bash
set -e

# 1. Очищаем переменную от невидимых символов Windows (\r), если они есть
APP_ENV=$(echo "$APP_ENV" | tr -d '\r')

# 2. Если PORT не задан в docker-compose, используем 8000 по умолчанию
PORT=${PORT:-8000}

echo "[entrypoint] Environment: $APP_ENV"
echo "[entrypoint] Port: $PORT"

python manage.py collectstatic --noinput || true
python manage.py migrate || true

if [ "$APP_ENV" = "prod" ]; then
    echo "[entrypoint] Starting Gunicorn (PROD)..."
    exec gunicorn novatexapi.wsgi:application --bind 0.0.0.0:$PORT --workers 3
else
    echo "[entrypoint] Starting Django dev server (DEV)..."
    exec python manage.py runserver 0.0.0.0:$PORT
fi
