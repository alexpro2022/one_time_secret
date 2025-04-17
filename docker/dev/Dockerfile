# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12


FROM python:${PYTHON_VERSION}-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app


FROM base AS test
# Test =============
COPY pyproject.toml .
RUN python -m pip install --upgrade pip && pip install .[test]
COPY tests tests
# App ==============
COPY src src


FROM base AS app
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    python -m pip install --upgrade pip && pip install .
# User ========
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
# Migration ========
COPY alembic.ini .
COPY alembic alembic
# App ==============
COPY src src
