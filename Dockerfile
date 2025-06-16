FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gcc \
    musl-dev \
    libgirepository1.0-dev \
    libpango1.0-0 && \
    pip3 install uwsgi --no-cache-dir && \
    pip3 install poetry


WORKDIR /app/
COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root --without dev

COPY . .

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["uwsgi", "--ini", "infra/uwsgi.ini"]
