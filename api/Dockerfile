FROM camptocamp/c2cwsgiutils:3
MAINTAINER Camptocamp "info@camptocamp.com"

# Doing things in two steps to avoid needing to re-install everything when we do a rebuild
# after changing code

# Step #1 copy only the stuff needed to install the dependencies and run the script
WORKDIR /app
COPY *.txt /app/
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV MAPFISH_LOG_LEVEL=INFO \
    C2CWSGI_LOG_LEVEL=INFO \
    ALEMBIC_LOG_LEVEL=INFO \
    SQLALCHEMY_POOL_SIZE=5 \
    SQLALCHEMY_MAX_OVERFLOW=25 \
    GUNICORN_PARAMS="-b :8080 --worker-class gthread --threads 10 --workers 1"

# Step #2 copy the rest of the files (watch for the .dockerignore)
COPY . /app

ARG GIT_HASH
RUN pip install --no-cache-dir -e . && \
    flake8 /app/mapfish_print_logs /app/*.py && \
    c2cwsgiutils_genversion.py $GIT_HASH && \
    python -m compileall -q . /usr/local/lib/python3.7

# www-data
USER 33
