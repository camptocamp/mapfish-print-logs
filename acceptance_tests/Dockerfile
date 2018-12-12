FROM camptocamp/c2cwsgiutils:2-light
LABEL maintainer "info@camptocamp.org"

ARG DOCKER_VERSION=1.12.0
ARG DOCKER_COMPOSE_VERSION=1.10.0

WORKDIR /acceptance_tests

ENV DOCKER_RUN=1 \
    PYTHONPATH=/acceptance_tests

# Install all Debian dependencies except nodejs which requires https transport
RUN DOCKER_VERSION=${DOCKER_VERSION} \
    DOCKER_COMPOSE_VERSION=${DOCKER_COMPOSE_VERSION} \
    /opt/c2cwsgiutils/install_docker.sh

COPY . ./

RUN flake8 acceptance
CMD py.test -vv --color=yes --junitxml /reports/acceptance.xml acceptance
