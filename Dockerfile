# syntax=docker/dockerfile:1
FROM python:3.11-slim

# 1. Базовые переменные Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 2. Установка системных зависимостей
# ВАЖНО: Добавили 'dos2unix', чтобы чинить скрипты из Windows
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl git dos2unix postgresql-client \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Установка Python-зависимостей (кэширование)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
 && pip install -r /app/requirements.txt

# 4. Копируем код проекта
COPY . /app

# 5. Настройка Entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# МАГИЯ: Превращаем Windows (CRLF) в Linux (LF) принудительно
RUN dos2unix /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh

# Настройки по умолчанию
ENV APP_ENV=dev \
    DJANGO_SETTINGS_MODULE=novatexapi.settings \
    PORT=8000

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]