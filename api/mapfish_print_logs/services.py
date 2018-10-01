from c2cwsgiutils import services
from pyramid.httpexceptions import HTTPNotFound
import sqlalchemy as sa

from . import elastic_search
from .models import DBSession, PrintAccounting

ref_service = services.create("ref", "/ref")
source_service = services.create("source", "/source")
LIMIT = 2


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


@source_service.get(renderer='templates/source.html.mako')
def get_source(request):
    source = request.params['source']
    secret = request.params['secret']
    # TODO: authenticate: request.params['secret']
    pos = int(request.params.get('pos', '0'))
    logs = DBSession.query(PrintAccounting).filter(
        sa.or_(
            PrintAccounting.app_id == source,
            PrintAccounting.app_id.like(source.replace("%", "\%").replace("_", "\_") + ":%")
        )
    ).order_by(PrintAccounting.completion_time.desc()).offset(pos).limit(LIMIT+1).all()
    return {
        'source': source,
        'secret': secret,
        'jobs': [log.to_json() for log in logs[:LIMIT]],
        'next_pos': None if len(logs) <= LIMIT else pos + LIMIT,
        'prev_pos': None if pos == 0 else max(0, pos - LIMIT)
    }
