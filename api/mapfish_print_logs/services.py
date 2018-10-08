from c2cwsgiutils import services
import os
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
import yaml
import sqlalchemy as sa

from . import elastic_search
from .models import DBSession, PrintAccounting

ref_service = services.create("ref", "/ref")
source_service = services.create("source", "/source")
LIMIT = 10
SHARED_CONFIG_MASTER = os.environ['SHARED_CONFIG_MASTER']


@ref_service.get(renderer='templates/ref.html.mako')
def get_ref(request):
    ref = request.params['ref']
    accounting = DBSession.query(PrintAccounting).get(ref)
    if accounting is None:
        raise HTTPNotFound("No such ref")
    return {
        'ref': ref,
        'logs': elastic_search.get_logs(ref),
        'accounting': accounting
    }


def _quote_like(text):
    return text.replace("%", "\%").replace("_", "\_")


@source_service.post(renderer='templates/source.html.mako')
def get_source(request):
    source = request.params['source']
    key = request.params['key']
    check_key(source, key)
    pos = int(request.params.get('pos', '0'))
    logs = DBSession.query(PrintAccounting).filter(
        sa.or_(
            PrintAccounting.app_id == source,
            PrintAccounting.app_id.like(_quote_like(source) + ":%")
        )
    ).order_by(PrintAccounting.completion_time.desc()).offset(pos).limit(LIMIT+1).all()
    return {
        'source': source,
        'secret': key,
        'jobs': [log for log in logs[:LIMIT]],
        'next_pos': None if len(logs) <= LIMIT else pos + LIMIT,
        'prev_pos': None if pos == 0 else max(0, pos - LIMIT)
    }


def check_key(source, secret):
    secrets = read_keys()
    if source not in secrets:
        raise HTTPNotFound("No such source")
    if secret != secrets[source]:
        raise HTTPForbidden("Invalid secret")


def read_keys():
    with open(SHARED_CONFIG_MASTER) as file:
        config = yaml.load(file)
    return {name: source['key'] for name, source in config['sources'].items()}
