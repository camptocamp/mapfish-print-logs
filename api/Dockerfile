FROM ubuntu:20.04 AS base
LABEL maintainer "info@camptocamp.org"

RUN apt update && \
  DEBIAN_FRONTEND=noninteractive apt install --assume-yes --no-install-recommends \
  python3-pip python3-dev gcc libpq-dev postgresql-client && \
  apt clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache/*

# Doing things in two steps to avoid needing to re-install everything when we do a rebuild
# after changing code

# Step #1 copy only the stuff needed to install the dependencies and run the script
WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m pip install --disable-pip-version-check --no-cache-dir --requirement=requirements.txt
COPY Pipfile Pipfile.lock /app/
RUN pipenv sync --system --clear
RUN apt remove --assume-yes --auto-remove python3-dev gcc

# From c2cwsgiutils

CMD ["gunicorn", "--paste=production.ini"]

ENV TERM=linux \
  LANG=C.UTF-8 \
  LOG_TYPE=console \
  LOG_HOST=localhost \
  LOG_PORT=514 \
  SQL_LOG_LEVEL=WARN \
  GUNICORN_LOG_LEVEL=WARN \
  OTHER_LOG_LEVEL=WARN \
  DEVELOPMENT=0 \
  PKG_CONFIG_ALLOW_SYSTEM_LIBS=OHYESPLEASE

ENV C2C_BASE_PATH=/logs/c2c \
  C2C_SECRET= \
  C2C_REDIS_URL= \
  C2C_REDIS_SENTINELS= \
  C2C_REDIS_TIMEOUT=3 \
  C2C_REDIS_SERVICENAME=mymaster \
  C2C_REDIS_DB=0 \
  C2C_BROADCAST_PREFIX=broadcast_api_ \
  C2C_REQUEST_ID_HEADER= \
  C2C_REQUESTS_DEFAULT_TIMEOUT= \
  C2C_SQL_PROFILER_ENABLED=1 \
  C2C_PROFILER_PATH= \
  C2C_PROFILER_MODULES= \
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
    SQLALCHEMY_WARN_20=true


FROM base as checker

RUN pipenv sync --dev --system --clear

COPY . /app

RUN prospector --output=pylint


FROM base as runner

COPY . /app

ARG GIT_HASH
RUN python3 -m pip install --no-cache-dir --no-deps --editable=.

RUN c2cwsgiutils-genversion $GIT_HASH && \
    python3 -m compileall -q . /usr/local/lib/python3.* \
    -x /usr/local/lib/python3.*/dist-packages/pipenv/

EXPOSE 8080
# www-data
USER 33
