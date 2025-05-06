FROM python:3.12.4

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

    WORKDIR /app

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock* /app/


RUN poetry install --no-root

COPY . /app/

EXPOSE 8090

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090", "--reload"]
