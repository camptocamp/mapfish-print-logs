from c2cwsgiutils import services
from pyramid.httpexceptions import HTTPNotFound

from mapfish_print_logs import elastic_search
from mapfish_print_logs.config import LOG_LIMIT, MAX_LOGS
from mapfish_print_logs.models import DBSession, PrintAccounting
from mapfish_print_logs.utils import app_id2source

ref_service = services.create("ref", "/logs/ref")


@ref_service.get(renderer="../templates/ref.html.mako")
def get_ref(request):
    ref = request.params["ref"]
    pos = int(request.params.get("pos", "0"))
    min_level = int(request.params.get("min_level", "20000"))
    filter_loggers = request.params.get("filter_loggers", "")
    if filter_loggers != "":
        filter_loggers = filter_loggers.split(",")
    else:
        filter_loggers = []
    accounting = DBSession.query(PrintAccounting).get(ref)  # type: PrintAccounting
    if accounting is None:
        raise HTTPNotFound("No such ref")
    logs, total = elastic_search.get_logs(ref, min_level, pos, LOG_LIMIT, filter_loggers)
    return {
        "ref": ref,
        "min_level": min_level,
        "logs": logs,
        "accounting": accounting,
        "cur_pos": pos,
        "next_pos": None if len(logs) + pos >= total else pos + LOG_LIMIT,
        "prev_pos": None if pos == 0 else max(0, pos - LOG_LIMIT),
        "last_pos": None
        if len(logs) + pos >= total
        else ((min(total, MAX_LOGS) - 1) // LOG_LIMIT) * LOG_LIMIT,
        "limit": LOG_LIMIT,
        "total": total,
        "max_logs": MAX_LOGS,
        "filter_loggers": filter_loggers,
        "source": app_id2source(accounting.app_id) if request.key is not None else None,
    }
