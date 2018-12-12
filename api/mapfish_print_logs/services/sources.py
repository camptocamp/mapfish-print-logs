from c2cwsgiutils import services
import copy
from pyramid.httpexceptions import HTTPForbidden, HTTPBadRequest

from . import read_shared_config, SOURCES_KEY

sources_service = services.create("sources", "/logs/sources")


@sources_service.post(renderer='../templates/sources.html.mako')
@sources_service.get(renderer='../templates/sources.html.mako')
def get_sources(request):
    key = request.params.get('key')
    if key is None:
        raise HTTPBadRequest("Missing the key")
    if key != SOURCES_KEY:
        raise HTTPForbidden("Invalid secret")
    config = read_shared_config()
    sources = []
    for name, config in config['sources'].items():
        source = copy.deepcopy(config)
        source['id'] = name
        sources.append(source)

    return dict(key=key, sources=sorted(sources, key=lambda s: s['id']))
