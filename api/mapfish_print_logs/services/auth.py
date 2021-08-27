from typing import Dict

import pyramid.request  # type: ignore
import pyramid.response  # type: ignore
from c2cwsgiutils import services
from pyramid.renderers import render_to_response  # type: ignore
from pyramid.security import forget, remember  # type: ignore

from mapfish_print_logs import utils
from mapfish_print_logs.services import SOURCES_KEY

login_service = services.create("login", "/logs/login")
logout_service = services.create("logout", "/logs/logout")


@login_service.get(renderer="../templates/login.html.mako")  # type: ignore
def login(request: pyramid.request.Request) -> Dict[str, str]:
    return dict(back=request.params.get("back", ""), message="")


@login_service.post()  # type: ignore
def do_login(request: pyramid.request.Request) -> pyramid.response.Response:
    key = request.params.get("key")
    back = request.params.get("back", "")

    key_ok = key == SOURCES_KEY

    if not key_ok:
        config = utils.read_shared_config()
        for config in config["sources"].values():
            if config["key"] == key:
                key_ok = True
                break

    if key_ok:
        response = request.response
        response.headerlist.extend(remember(request, key))
        response.status_code = 302
        response.headers["Location"] = back if back else "/logs/"
        return response
    return render_to_response(
        "../templates/login.html.mako",
        dict(back=back, message="Invalid key"),
        request=request,
    )


@logout_service.get()  # type: ignore
def do_logout(request: pyramid.request.Request) -> pyramid.response.Response:
    response = request.response
    response.headerlist.extend(forget(request))
    response.status_code = 302
    response.headers["Location"] = "/logs/"
    return response
