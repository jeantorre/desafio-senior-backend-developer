FROM python:3.12.4 AS base
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install --no-cache-dir poetry
ENV POETRY_VIRTUALENVS_CREATE=false
COPY backend/pyproject.toml backend/poetry.lock* /app/
RUN poetry install --no-root


FROM base AS development
COPY backend /app/
COPY tests /app/tests
ENV PYTHONPATH=/app

FROM base AS production
COPY backend /app/
ENV PYTHONPATH=/app
