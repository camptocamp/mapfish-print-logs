FROM ubuntu:22.04
LABEL maintainer Camptocamp "info@camptocamp.com"
SHELL ["/bin/bash", "-o", "pipefail", "-cux"]

COPY shared_config_manager.yaml /master_config/master/shared_config_manager.yaml
COPY print-apps /usr/local/tomcat/webapps/ROOT/print-apps

VOLUME /master_config
VOLUME /usr/local/tomcat/webapps/ROOT/print-apps

USER 33
