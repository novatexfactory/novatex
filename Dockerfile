# syntax=docker/dockerfile:1
FROM python:3.11-slim

# --------------------------
# Basic Environment
# --------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# --------------------------
# System Dependencies
# --------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl git \
 && rm -rf /var/lib/apt/lists/*

# --------------------------
# Work Directory
# --------------------------
WORKDIR /app

# --------------------------
# Install Python Dependencies First (for better caching)
# --------------------------
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
 && pip install -r /app/requirements.txt

# --------------------------
# Copy Project Code
# --------------------------
COPY . /app

# --------------------------
# Default Environment Variables
# (can be overridden by docker-compose)
# --------------------------
ENV APP_ENV=dev \
    DJANGO_SETTINGS_MODULE=novatexapi.settings \
    PORT=8000

# --------------------------
# Expose Django Port
# --------------------------
EXPOSE 8000

# --------------------------
# Entrypoint
# --------------------------
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
