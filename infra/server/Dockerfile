FROM python:3.12-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Amsterdam \
    PATH=/venv/bin:$PATH 

WORKDIR /app


FROM base AS build-venv

RUN pip install "poetry==1.8.2"

RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./

ENV VIRTUAL_ENV=/venv

RUN poetry install --without dev


FROM base AS production

EXPOSE 8000

COPY --from=build-venv /venv /venv
COPY server/app /app

RUN adduser --system --uid 5678 appuser

USER appuser

CMD ["fastapi", "run", "main.py", "--workers", "2"]
