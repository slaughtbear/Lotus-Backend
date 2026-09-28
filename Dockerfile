FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /uvx /bin/

WORKDIR /code

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

FROM python:3.13-slim

RUN useradd --create-home appuser

WORKDIR /code

COPY --from=builder /code/.venv /code/.venv
COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini

ENV PATH="/code/.venv/bin:$PATH"

USER appuser

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]