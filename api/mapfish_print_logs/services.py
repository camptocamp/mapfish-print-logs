from c2cwsgiutils import services
import copy
import os
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPBadRequest
import yaml
import sqlalchemy as sa
import requests

from . import elastic_search
from .config import SCM_URL, SCM_URL_EXTERNAL, JOB_LIMIT, SHARED_CONFIG_MASTER, LOG_LIMIT
from .models import DBSession, PrintAccounting

ref_service = services.create("ref", "/logs/ref")
source_service = services.create("source", "/logs/source")
sources_service = services.create("sources", "/logs/sources")
auth_source_service = services.create("source_auth", "/logs/source/{source}/{key}")
SOURCES_KEY = os.environ['SOURCES_KEY']


@ref_service.get(renderer='templates/ref.html.mako')
def get_ref(request):
    ref = request.params['ref']
    pos = int(request.params.get('pos', '0'))
    min_level = int(request.params.get('min_level', '20000'))
    accounting = DBSession.query(PrintAccounting).get(ref)  # type: PrintAccounting
    if accounting is None:
        raise HTTPNotFound("No such ref")
    logs, total = elastic_search.get_logs(ref, min_level, pos, LOG_LIMIT)
    print(total)
    return {
        'ref': ref,
        'min_level': min_level,
        'logs': logs,
        'accounting': accounting,
        'cur_pos': pos,
        'next_pos': None if len(logs) + pos >= total else pos + LOG_LIMIT,
        'prev_pos': None if pos == 0 else max(0, pos - LOG_LIMIT),
        'last_pos': None if len(logs) + pos >= total else ((total - 1) // LOG_LIMIT) * LOG_LIMIT,
        'limit': LOG_LIMIT,
        'total': total
    }


def _quote_like(text):
    return text.replace("%", r"\%").replace("_", r"\_")


@source_service.post(renderer='templates/source.html.mako')
@auth_source_service.get(renderer='templates/source.html.mako')
def get_source(request):
    source = request.matchdict.get('source', request.params.get('source'))
    if source is None:
        raise HTTPBadRequest("Missing the source")
    key = request.matchdict.get('key', request.params.get('key'))
    if key is None:
        raise HTTPBadRequest("Missing the key")
    config = _read_shared_config()
    check_key(config, source, key)
    pos = int(request.params.get('pos', '0'))
    app_id = _get_app_id(config, source)
    logs = DBSession.query(PrintAccounting).filter(
        sa.or_(
            PrintAccounting.app_id == app_id,
            PrintAccounting.app_id.like(_quote_like(app_id) + ":%")
        )
    ).order_by(PrintAccounting.completion_time.desc()).offset(pos).limit(JOB_LIMIT + 1).all()

    return {
        'source': source,
        'key': key,
        'jobs': [log for log in logs[:JOB_LIMIT]],
        'scm_refresh_url': f'{SCM_URL_EXTERNAL}1/refresh/{source}/{key}' if SCM_URL_EXTERNAL is not None
                           else None,
        'config': _get_config_info(source, key),
        'next_pos': None if len(logs) <= JOB_LIMIT else pos + JOB_LIMIT,
        'prev_pos': None if pos == 0 else max(0, pos - JOB_LIMIT)
    }


def _get_app_id(config, source):
    source_config = config['sources'][source]
    return source_config.get('app_id', source)


def check_key(config, source, secret):
    if source not in config['sources']:
        raise HTTPNotFound("No such source")
    if secret != config['sources'][source]['key']:
        raise HTTPForbidden("Invalid secret")


def _read_shared_config():
    with open(SHARED_CONFIG_MASTER) as file:
        config = yaml.load(file)
    return config


def _get_config_info(source, key):
    if SCM_URL is None:
        return None
    try:
        r = requests.get(f'{SCM_URL}1/status/{source}/{key}')
    except Exception as e:
        return dict(status=500, message=str(e))
    if r.status_code != 200:
        return dict(status=r.status_code, message=r.text)
    return r.json()


@sources_service.post(renderer='templates/sources.html.mako')
@sources_service.get(renderer='templates/sources.html.mako')
def get_sources(request):
    key = request.params.get('key')
    if key is None:
        raise HTTPBadRequest("Missing the key")
    if key != SOURCES_KEY:
        raise HTTPForbidden("Invalid secret")
    config = _read_shared_config()
    sources = []
    for name, config in config['sources'].items():
        source = copy.deepcopy(config)
        source['id'] = name
        sources.append(source)

    return dict(key=key, sources=sorted(sources, key=lambda s: s['id']))
