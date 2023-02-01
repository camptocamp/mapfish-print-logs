"""
Setup of the Pyramid application
"""

import logging
from typing import Any, Dict

import c2cwsgiutils.pyramid
import pyramid.request  # type: ignore
import pyramid.response  # type: ignore
import sqlalchemy
from c2cwsgiutils.health_check import HealthCheck
from pyramid.config import Configurator  # type: ignore

import mapfish_print_logs.security
from mapfish_print_logs.config import SCM_URL
from mapfish_print_logs.elastic_search import SEARCH_HEADERS, SEARCH_URL

LOG = logging.getLogger(__name__)


def forbidden(request: pyramid.request.Request) -> pyramid.response.Response:
    is_auth = c2cwsgiutils.auth.is_auth(request)

    if is_auth:
        return pyramid.httpexceptions.HTTPForbidden(request.exception.message)
    return pyramid.httpexceptions.HTTPFound(
        location=request.route_url(
            "c2c_github_login",
            _query={"came_from": request.current_route_url()},
        )
    )


def main(_: Any, **settings: Dict[str, Any]) -> Any:
    """This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.include(c2cwsgiutils.pyramid.includeme)
    config.include("pyramid_mako")
    dbsession = c2cwsgiutils.db.init(config, "sqlalchemy", "sqlalchemy_slave")
    config.set_security_policy(mapfish_print_logs.security.SecurityPolicy())
    config.add_forbidden_view(forbidden)

    health_check = HealthCheck(config)
    health_check.add_db_session_check(
        dbsession, query_cb=lambda session: session.execute(sqlalchemy.text("SELECT 1")).fetchall()[0][0]
    )
    if SCM_URL is not None:
        health_check.add_url_check(SCM_URL + "c2c/health_check", name="scm", level=3)
    health_check.add_url_check(
        SEARCH_URL,
        params=dict(size="0"),
        headers=SEARCH_HEADERS,
        check_cb=lambda request, response: response.json(),
        name="elasticsearch",
        level=3,
    )

    config.scan("mapfish_print_logs.services")
    config.add_static_view(name="/", path="/app/mapfish_print_logs/static", cache_max_age=0)

    return config.make_wsgi_app()
