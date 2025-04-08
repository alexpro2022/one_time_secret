# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12


FROM python:${PYTHON_VERSION}-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN --mount=type=bind,source=requirements,target=requirements \
    python -m pip install --upgrade pip && \
    pip install -r requirements/requirements.txt --no-cache-dir


FROM base AS test
RUN --mount=type=bind,source=requirements,target=requirements \
    pip install -r requirements/test.requirements.txt --no-cache-dir
COPY src src
COPY setup.cfg .
COPY tests tests


FROM base AS migration
RUN pip install alembic
COPY alembic.ini .
COPY alembic alembic


FROM migration AS app
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
COPY src src
