import os
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPBadRequest
import requests
import yaml

from ..config import SCM_URL, SHARED_CONFIG_MASTER

SOURCES_KEY = os.environ['SOURCES_KEY']


def auth_source(request):
    source = request.matchdict.get('source', request.params.get('source'))
    if source is None:
        raise HTTPBadRequest("Missing the source")
    key = request.matchdict.get('key', request.params.get('key'))
    if key is None:
        raise HTTPBadRequest("Missing the key")
    config = read_shared_config()
    check_key(config, source, key)
    return config, key, source


def read_shared_config():
    with open(SHARED_CONFIG_MASTER) as file:
        config = yaml.load(file)
    return config


def check_key(config, source, secret):
    if source not in config['sources']:
        raise HTTPNotFound("No such source")
    if secret != config['sources'][source]['key']:
        raise HTTPForbidden("Invalid secret")


def get_config_info(source, key):
    if SCM_URL is None:
        return None
    try:
        r = requests.get(f'{SCM_URL}1/status/{source}/{key}')
    except Exception as e:
        return dict(status=500, message=str(e))
    if r.status_code != 200:
        return dict(status=r.status_code, message=r.text)
    return r.json()
