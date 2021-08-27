import copy
from typing import Any, Dict

import pyramid.request  # type: ignore
from c2cwsgiutils import services

from mapfish_print_logs import utils
from mapfish_print_logs.services import SOURCES_KEY

login_service = services.create("index", "/logs/")


@login_service.get(renderer="../templates/index.html.mako")  # type: ignore
def index(request: pyramid.request.Request) -> Dict[str, Any]:
    key = request.key
    is_auth = key is not None
    is_admin = is_auth and key == SOURCES_KEY

    sources = []
    if is_auth:
        config = utils.read_shared_config()
        for name, config in config["sources"].items():
            if is_admin or config["key"] == key:
                source = copy.deepcopy(config)
                source["id"] = name
                sources.append(source)

    def get_id(source: Dict[str, int]) -> int:
        return source["id"]

    return {"is_auth": is_auth, "is_admin": is_admin, "sources": list(sorted(sources, key=get_id))}
