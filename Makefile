DOCKER_TAG ?= latest
DOCKER_BASE = camptocamp/mapfish_print_logs
GIT_HASH := $(shell git rev-parse HEAD)

#Get the docker version (must use the same version for acceptance tests)
DOCKER_VERSION_ACTUAL := $(shell docker version --format '{{.Server.Version}}')
ifeq ($(DOCKER_VERSION_ACTUAL),)
DOCKER_VERSION := 1.12.0
else
DOCKER_VERSION := $(DOCKER_VERSION_ACTUAL)
endif

#Get the docker-compose version (must use the same version for acceptance tests)
DOCKER_COMPOSE_VERSION_ACTUAL := $(shell docker-compose version --short)

ifeq ($(DOCKER_COMPOSE_VERSION_ACTUAL),)
DOCKER_COMPOSE_VERSION := 1.10.0
else
DOCKER_COMPOSE_VERSION := $(DOCKER_COMPOSE_VERSION_ACTUAL)
endif

DOCKER_TTY := $(shell [ -t 0 ] && echo -ti)

all: build

.PHONY: pull
pull:
	for image in `find -name Dockerfile | xargs grep --no-filename FROM | awk '{print $$2}' | sort -u`; do docker pull $$image; done

.venv/timestamp: api/requirements.txt Makefile
	/usr/bin/virtualenv --python=/usr/bin/python3 .venv
	.venv/bin/pip install -r api/requirements.txt
	touch $@

build: build_api build_configs

.PHONY: build_api
build_api:
	docker build -t $(DOCKER_BASE):$(DOCKER_TAG) --build-arg "GIT_HASH=$(GIT_HASH)" api

.PHONY: build_configs
build_configs:
	docker build -t $(DOCKER_BASE)_configs:$(DOCKER_TAG) --build-arg "GIT_HASH=$(GIT_HASH)" configs

.PHONY: build_acceptance
build_acceptance:
	docker build --build-arg DOCKER_VERSION="$(DOCKER_VERSION)" --build-arg DOCKER_COMPOSE_VERSION="$(DOCKER_COMPOSE_VERSION)" -t $(DOCKER_BASE)_acceptance:$(DOCKER_TAG) acceptance_tests

run: build
	docker-compose -p logs stop && \
	docker-compose -p logs rm -f && \
	docker-compose -p logs up

.PHONY: acceptance
acceptance: build_acceptance build
	rm -rf reports/coverage/api reports/acceptance*.xml
	mkdir -p reports/coverage/api
	#run the tests
	docker run $(DOCKER_TTY) -e DOCKER_TAG=$(DOCKER_TAG) -v /var/run/docker.sock:/var/run/docker.sock --name logs_acceptance_$(DOCKER_TAG)_$$PPID $(DOCKER_BASE)_acceptance:$(DOCKER_TAG) \
	bash -c "py.test -vv --color=yes --junitxml /reports/acceptance.xml $(PYTEST_OPTS) acceptance; status=\$$?; junit2html /reports/acceptance.xml /reports/acceptance.html; exit \$$status\$$?"; \
	status=$$status$$?; \
	#copy the reports locally \
	docker cp logs_acceptance_$(DOCKER_TAG)_$$PPID:/reports ./; \
	status=$$status$$?; \
	docker rm logs_acceptance_$(DOCKER_TAG)_$$PPID; \
	#status=$$status$$?; \
	##generate the HTML report for code coverage \
	#docker run -v $(THIS_DIR)/reports/coverage/api:/reports/coverage/api:ro --name logs_acceptance_reports_$(DOCKER_TAG)_$$PPID $(DOCKER_BASE):$(DOCKER_TAG) c2cwsgiutils_coverage_report.py; \
	#status=$$status$$?; \
	##copy the HTML locally \
	#docker cp logs_acceptance_reports_$(DOCKER_TAG)_$$PPID:/tmp/coverage/api reports/coverage; \
	#status=$$status$$?; \
	#docker rm logs_acceptance_reports_$(DOCKER_TAG)_$$PPID; \
	exit $$status$$?
