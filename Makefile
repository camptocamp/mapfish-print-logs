DOCKER_TAG ?= latest
DOCKER_BASE = camptocamp/mapfish_print_logs
GIT_HASH := $(shell git rev-parse HEAD)

sll: build

.PHONY: pull
pull:
	for image in `find -name Dockerfile | xargs grep --no-filename FROM | awk '{print $$2}' | sort -u`; do docker pull $$image; done

.venv/timestamp: api/requirements.txt Makefile
	/usr/bin/virtualenv --python=/usr/bin/python3 .venv
	.venv/bin/pip install -r api/requirements.txt
	touch $@

.PHONY: build
build:
	docker build -t $(DOCKER_BASE):$(DOCKER_TAG) --build-arg "GIT_HASH=$(GIT_HASH)" api


run: build
	docker-compose -p logs stop && \
	docker-compose -p logs rm -f && \
	docker-compose -p logs up
