import logging
import os
from typing import Any, Dict, Optional, Tuple, cast

import pyramid.request  # type: ignore
import requests
from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound  # type: ignore

from mapfish_print_logs.config import SCM_URL
from mapfish_print_logs.utils import read_shared_config

SOURCES_KEY = os.environ["SOURCES_KEY"]
LOG = logging.getLogger(__name__)


def auth_source(request: pyramid.request.Request) -> Tuple[Dict[str, Any], str, str]:
    source = request.matchdict.get("source")
    if source is None:
        raise HTTPBadRequest("Missing the source")
    key = request.authenticated_userid
    config = read_shared_config()
    check_key(config, source, key)
    return config, key, source


def check_key(config: Dict[str, Any], source: str, secret: str) -> None:
    if source == "all":
        if secret != SOURCES_KEY:
            raise HTTPForbidden("Invalid secret")
        return
    if source not in config["sources"]:
        raise HTTPNotFound("No such source")
    if secret not in (SOURCES_KEY, config["sources"][source]["key"]):
        raise HTTPForbidden("Invalid secret")


def get_config_info(source: str, key: str) -> Optional[Dict[str, Any]]:
    if SCM_URL is None:
        return None
    url = f"{SCM_URL}1/status/{source}/{key}"
    try:
        response = requests.get(url)
    except Exception:  # pylint: disable=broad-except
        LOG.exception("Error in request: %s", url)
        return dict(status=500, message="Error in subrequest, see logs for details")
    if response.status_code != 200:
        return dict(status=response.status_code, message=response.text)
    return cast(Dict[str, Any], response.json())
