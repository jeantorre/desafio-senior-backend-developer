FROM python:3.12.4 as base
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install --no-cache-dir poetry
ENV POETRY_VIRTUALENVS_CREATE=false
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root


FROM base as development
COPY . /app/
COPY tests /app/tests/

FROM base as production
COPY . /app/
