#!/bin/bash
set -e

echo "[entrypoint] Environment: $APP_ENV"
python manage.py collectstatic --noinput || true
python manage.py migrate || true

if [ "$APP_ENV" = "prod" ]; then
    echo "[entrypoint] Starting Gunicorn..."
    exec gunicorn novatexapi.wsgi:application --bind 0.0.0.0:$PORT --workers 3
else
    echo "[entrypoint] Starting Django dev server..."
    exec python manage.py runserver 0.0.0.0:$PORT
fi
