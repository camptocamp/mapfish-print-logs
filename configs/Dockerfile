FROM ubuntu:20.04

COPY shared_config_manager.yaml /master_config/master/shared_config_manager.yaml
COPY print-apps /usr/local/tomcat/webapps/ROOT/print-apps

VOLUME /master_config
VOLUME /usr/local/tomcat/webapps/ROOT/print-apps

USER 33
