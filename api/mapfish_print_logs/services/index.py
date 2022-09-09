import copy
from typing import Any, Dict

import pyramid.request  # type: ignore
from c2cwsgiutils import services

from mapfish_print_logs import utils
from mapfish_print_logs.configuration import SourceConfig

login_service = services.create("index", "/")


@login_service.get(renderer="../templates/index.html.mako")  # type: ignore
def index(request: pyramid.request.Request) -> Dict[str, Any]:
    sources = []
    if request.identity is not None and request.identity.is_auth:
        full_config = utils.read_shared_config()
        for name, config in full_config["sources"].items():
            if request.has_permission("all", config):
                source = copy.deepcopy(config)
                source["id"] = name
                sources.append(source)

    def get_id(source: SourceConfig) -> str:
        return source["id"] or ""

    return {
        "sources": list(sorted(sources, key=get_id)),
    }
