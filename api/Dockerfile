FROM ubuntu:22.04 AS base-all
LABEL maintainer Camptocamp "info@camptocamp.com"
SHELL ["/bin/bash", "-o", "pipefail", "-cux"]

RUN --mount=type=cache,target=/var/lib/apt/lists \
    --mount=type=cache,target=/var/cache,sharing=locked \
    apt-get update \
    && apt-get upgrade --assume-yes \
    && apt-get install --assume-yes --no-install-recommends python3-pip

# Used to convert the locked packages by poetry to pip requirements format
# We don't directly use `poetry install` because it force to use a virtual environment.
FROM base-all as poetry

# Install Poetry
WORKDIR /tmp
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache \
    python3 -m pip install --disable-pip-version-check --requirement=requirements.txt

# Do the conversion
COPY poetry.lock pyproject.toml ./
RUN poetry export --output=requirements.txt \
    && poetry export --with=dev --output=requirements-dev.txt

# Base, the biggest thing is to install the Python packages
FROM base-all as base

RUN --mount=type=cache,target=/var/lib/apt/lists \
    --mount=type=cache,target=/var/cache,sharing=locked \
    apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        curl python3-dev gcc libpq-dev postgresql-client

# Doing things in two steps to avoid needing to re-install everything when we do a rebuild
# after changing code

# Step #1 copy only the stuff needed to install the dependencies and run the script
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,from=poetry,source=/tmp,target=/poetry \
    python3 -m pip install --disable-pip-version-check --no-deps --requirement=/poetry/requirements.txt \
    && apt-get remove --assume-yes --auto-remove python3-dev gcc

# From c2cwsgiutils

CMD ["gunicorn", "--paste=production.ini"]

ENV LOG_TYPE=console \
    LOG_HOST=localhost \
    LOG_PORT=514 \
    SQL_LOG_LEVEL=WARN \
    GUNICORN_LOG_LEVEL=WARN \
    OTHER_LOG_LEVEL=WARN \
    DEVELOPMENT=0

ENV C2C_BASE_PATH=/c2c \
    C2C_REDIS_TIMEOUT=3 \
    C2C_REDIS_SERVICENAME=mymaster \
    C2C_REDIS_DB=0 \
    C2C_BROADCAST_PREFIX=broadcast_api_ \
    C2C_SQL_PROFILER_ENABLED=1 \
    C2C_DEBUG_VIEW_ENABLED=1 \
    C2C_ENABLE_EXCEPTION_HANDLING=0 \
    C2C_LOG_VIEW_ENABLED=1 \
    C2C_REQUESTS_DEFAULT_TIMEOUT=10
# End from c2cwsgiutils

ENV LOG_LEVEL=INFO \
    C2CWSGIUTILS_LOG_LEVEL=INFO \
    ALEMBIC_LOG_LEVEL=INFO \
    GUNICORN_LOG_LEVEL=WARN \
    GUNICORN_ACCESS_LOG_LEVEL=INFO \
    SQLALCHEMY_POOL_SIZE=5 \
    SQLALCHEMY_MAX_OVERFLOW=25 \
    SQLALCHEMY_POOL_RECYCLE=30 \
    SQLALCHEMY_SLAVE_POOL_SIZE=5 \
    SQLALCHEMY_SLAVE_MAX_OVERFLOW=25 \
    SQLALCHEMY_SLAVE_POOL_RECYCLE=30 \
    SQLALCHEMY_WARN_20=true \
    VISIBLE_ENTRY_POINT=/logs

FROM base as checker

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,from=poetry,source=/tmp,target=/poetry \
    python3 -m pip install --disable-pip-version-check --no-deps --requirement=/poetry/requirements-dev.txt

COPY . /app

FROM base as runner

COPY . /app

ARG GIT_HASH
RUN --mount=type=cache,target=/root/.cache \
    python3 -m pip install --no-deps --editable=. \
    && python3 -m pip freeze > /requirements.txt \
    && c2cwsgiutils-genversion $GIT_HASH \
    && python3 -m compileall -q . /usr/local/lib/python3.*

EXPOSE 8080
# www-data
USER 33
