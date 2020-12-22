import os

import requests
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound

from mapfish_print_logs.config import SCM_URL
from mapfish_print_logs.utils import read_shared_config

SOURCES_KEY = os.environ["SOURCES_KEY"]


def auth_source(request):
    source = request.matchdict.get("source")
    if source is None:
        raise HTTPBadRequest("Missing the source")
    key = request.authenticated_userid
    config = read_shared_config()
    check_key(config, source, key)
    return config, key, source


def check_key(config, source, secret):
    if source == "all":
        if secret != SOURCES_KEY:
            raise HTTPForbidden("Invalid secret")
        return
    if source not in config["sources"]:
        raise HTTPNotFound("No such source")
    if secret not in (SOURCES_KEY, config["sources"][source]["key"]):
        raise HTTPForbidden("Invalid secret")


def get_config_info(source, key):
    if SCM_URL is None:
        return None
    try:
        r = requests.get(f"{SCM_URL}1/status/{source}/{key}")
    except Exception as e:
        return dict(status=500, message=str(e))
    if r.status_code != 200:
        return dict(status=r.status_code, message=r.text)
    return r.json()
