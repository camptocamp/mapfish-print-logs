from c2cwsgiutils import services
import copy

from . import SOURCES_KEY
from .. import utils

login_service = services.create("index", "/logs/")


@login_service.get(renderer='../templates/index.html.mako')
def index(request):
    key = request.key
    is_auth = key is not None
    is_admin = is_auth and key == SOURCES_KEY

    sources = []
    if is_auth:
        config = utils.read_shared_config()
        for name, config in config['sources'].items():
            if is_admin or config['key'] == key:
                source = copy.deepcopy(config)
                source['id'] = name
                sources.append(source)

    return {
        'is_auth': is_auth,
        'is_admin': is_admin,
        'sources': list(sorted(sources, key=lambda s: s['id']))
    }
