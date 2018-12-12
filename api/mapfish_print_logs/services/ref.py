from c2cwsgiutils import services
from pyramid.httpexceptions import HTTPNotFound

from .. import elastic_search
from ..models import DBSession, PrintAccounting
from ..config import LOG_LIMIT

ref_service = services.create("ref", "/logs/ref")


@ref_service.get(renderer='../templates/ref.html.mako')
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
