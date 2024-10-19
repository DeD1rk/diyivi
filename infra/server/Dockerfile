FROM python:3.12-alpine AS base

ENV TZ=Europe/Amsterdam \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app
RUN adduser --system --uid 5678 appuser -H

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-cache --no-dev

EXPOSE 8000

COPY server/app /app

USER appuser

CMD ["fastapi", "run", "main.py", "--workers", "2"]
