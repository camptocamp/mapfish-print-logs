from c2cwsgiutils import services
from pyramid.httpexceptions import HTTPNotFound
import sqlalchemy as sa

from . import elastic_search
from .models import DBSession, PrintAccounting

ref_service = services.create("ref", "/ref")
source_service = services.create("source", "/source")


@ref_service.get(renderer='templates/ref.html.mako')
def get_ref(request):
    ref = request.params['ref']
    accounting =  DBSession.query(PrintAccounting).get(ref)
    if accounting is None:
        raise HTTPNotFound("No such ref")
    return {
        'ref': ref,
        'logs': elastic_search.get_logs(ref),
        'accounting': accounting
    }


@source_service.get()
def get_source(request):
    # TODO: authenticate: request.params['secret']
    logs = DBSession.query(PrintAccounting).filter(
        sa.or_(
            PrintAccounting.app_id == request.params['source'],
            PrintAccounting.app_id.like(request.params['source'].replace("%", "\%").replace("_", "\_") + ":%")
        )
    ).order_by(PrintAccounting.completion_time.desc()).limit(10)
    return {
        'jobs': [log.to_json() for log in logs]
    }
