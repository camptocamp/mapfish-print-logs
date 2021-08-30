DOCKER_TAG ?= latest
DOCKER_BASE = camptocamp/mapfish-print-logs
GIT_HASH := $(shell git rev-parse HEAD)

DOCKER_COMPOSE_TTY := $(shell [ ! -t 0 ] && echo -T || true)

all: acceptance

.PHONY: pull
pull:
	for image in `find -name Dockerfile | xargs grep --no-filename FROM | awk '{print $$2}' | grep -v base | sort -u`; do docker pull $$image; done
	for image in `find -name "docker-compose*.yaml" | xargs grep --no-filename "^ *image:" | awk '{print $$2}' | sort -u | grep -v $(DOCKER_BASE)`; do echo docker pull $$image; done
	for image in `find -name "docker-compose*.yaml" | xargs grep --no-filename "^ *image:" | awk '{print $$2}' | sort -u | grep -v $(DOCKER_BASE)`; do docker pull $$image; done

.venv/timestamp: api/requirements.txt Makefile
	/usr/bin/virtualenv --python=/usr/bin/python3.7 .venv
	.venv/bin/pip install --upgrade -r api/requirements.txt
	touch $@

build: build_api build_configs

.PHONY: build_api
build_api:
	docker build --target=checker --tag=$(DOCKER_BASE):$(DOCKER_TAG) --build-arg=GIT_HASH=$(GIT_HASH) api
	docker build --tag=$(DOCKER_BASE):$(DOCKER_TAG) --build-arg=GIT_HASH=$(GIT_HASH) api

.PHONY: build_configs
build_configs:
	docker build --tag=$(DOCKER_BASE)-configs:$(DOCKER_TAG) configs

.PHONY: build_acceptance
build_acceptance:
	docker build --tag=$(DOCKER_BASE)-acceptance:$(DOCKER_TAG) acceptance_tests

run: build build_acceptance
	docker-compose stop
	rm -rf reports/coverage/api reports/acceptance*.xml
	mkdir -p reports/coverage/api
	chmod o+rw reports
	docker-compose up -d

.PHONY: acceptance
acceptance:
	rm -rf reports/coverage/api reports/acceptance*.xml
	mkdir -p reports/coverage/api
	# Run the tests
	docker-compose exec $(DOCKER_COMPOSE_TTY) run py.test --verbosity=2 --color=yes --junitxml /reports/acceptance.xml $(PYTEST_OPTS) acceptance
	docker-compose exec $(DOCKER_COMPOSE_TTY) run junit2html /reports/acceptance.xml /reports/acceptance.html
