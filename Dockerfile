# Используем официальный Python
FROM python:3.12-slim

# Устанавливаем зависимости для poetry
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости (без виртуального окружения)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# Копируем проект
COPY . /app

