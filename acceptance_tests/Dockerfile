FROM ubuntu:20.04
LABEL maintainer "info@camptocamp.org"

WORKDIR /acceptance_tests

ENV PYTHONPATH=/acceptance_tests

RUN apt update && \
  DEBIAN_FRONTEND=noninteractive apt install --assume-yes --no-install-recommends \
  python3-pip python3-dev libpq-dev gcc && \
  apt clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache/*

COPY . ./
RUN python3 -m pip install --disable-pip-version-check --no-cache-dir --requirement=requirements.txt
RUN pipenv sync --system --clear

CMD sleep infinity
