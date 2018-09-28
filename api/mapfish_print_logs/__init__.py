"""
Setup of the Pyramid application
"""
import c2cwsgiutils.pyramid
from c2cwsgiutils.health_check import HealthCheck
import logging
from pyramid.config import Configurator

LOG = logging.getLogger(__name__)


def main(_, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings,
                          route_prefix='/logs')
    config.include(c2cwsgiutils.pyramid.includeme)

    HealthCheck(config)
    config.scan("mapfish_print_logs.services")
    # config.add_static_view(name="static", path="/app/static/")
    return config.make_wsgi_app()
