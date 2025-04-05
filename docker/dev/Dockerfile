# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=bind,source=requirements,target=requirements \
    python -m pip install --upgrade pip && \
    pip install -r requirements/requirements.txt --no-cache-dir

# COPY config config
# COPY src src


FROM base AS test
RUN --mount=type=bind,source=requirements,target=requirements \
    pip install -r requirements/test.requirements.txt --no-cache-dir

# COPY config config
COPY src src
COPY setup.cfg .
COPY tests tests


FROM base AS migration
RUN pip install alembic
COPY alembic.ini .
COPY alembic alembic
# ENTRYPOINT alembic upgrade head
# alembic revision --autogenerate
# && alembic upgrade head
# ["alembic", "revision", "--autogenerate"]


# FROM migration AS app
FROM migration AS app
# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
# Switch to the non-privileged user to run the application.
USER appuser
# COPY config config
COPY src src
# COPY alembic.ini .
# COPY alembic alembic
#EXPOSE 8000



# TO REMOVE BELOW ==========================
# CMD uvicorn src.app:app --host=0.0.0.0 --port=8000
# CMD uvicorn 'app:app' --host=0.0.0.0 --port=8000

# docker build -t=app --target=app -f=docker/dev/Dockerfile .
# docker build -t=test --target=test -f=docker/dev/Dockerfile .
# docker images | head -5
# docker history back
# docker rmi back

# docker run --name=app -it --rm app
# docker run --name=test -it --rm test
# docker stop back
# docker rm back
