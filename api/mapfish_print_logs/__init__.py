"""
Setup of the Pyramid application
"""
import c2cwsgiutils.pyramid
from c2cwsgiutils.health_check import HealthCheck
import logging
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPMovedPermanently

from . import models

LOG = logging.getLogger(__name__)


def _redirect_home(request):
    return HTTPMovedPermanently(location='/logs/')


def main(_, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include(c2cwsgiutils.pyramid.includeme)
    config.include('pyramid_mako')
    models.init(config)

    health_check = HealthCheck(config)
    health_check.add_db_session_check(models.DBSession, query_cb=lambda session: session.execute("select 1"))

    config.scan("mapfish_print_logs.services")
    config.add_static_view(name="/logs", path="/app/mapfish_print_logs/static", cache_max_age=0)
    config.add_route(name='index', path='/logs')
    config.add_view(view=_redirect_home, route_name='index')

    return config.make_wsgi_app()
