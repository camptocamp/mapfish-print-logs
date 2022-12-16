import os
from typing import Any, Dict

import pyramid.request  # type: ignore
import sqlalchemy  # type: ignore
from c2cwsgiutils import services
from pyramid.httpexceptions import HTTPNotFound  # type: ignore
from pyramid.security import Allowed  # type: ignore

from mapfish_print_logs import elastic_search, loki, utils
from mapfish_print_logs.config import LOG_LIMIT, MAX_LOGS
from mapfish_print_logs.models import PrintAccounting
from mapfish_print_logs.security import auth_source
from mapfish_print_logs.utils import app_id2source

ref_service = services.create("ref", "/ref")


@ref_service.get(renderer="../templates/ref.html.mako")  # type: ignore
def get_ref(request: pyramid.request.Request) -> Dict[str, Any]:
    ref = request.params["ref"]
    pos = int(request.params.get("pos", "0"))
    debug = request.params.get("debug", "false").lower() in ("true", "yes", "1")
    filter_loggers = request.params.get("filter_loggers", "")
    if filter_loggers != "":
        filter_loggers = filter_loggers.split(",")
    else:
        filter_loggers = []

    if ref == "latest" and "source" in request.params:
        config, source = auth_source(request, request.params["source"])
        app_id = utils.get_app_id(config, source)
        query = request.dbsession.query(PrintAccounting.reference_id)
        query = query.filter(
            sqlalchemy.or_(
                PrintAccounting.app_id == app_id, PrintAccounting.app_id.like(utils.quote_like(app_id) + ":%")
            )
        )
        log = query.order_by(PrintAccounting.completion_time.desc()).limit(1).one_or_none()
        if log is not None:
            ref = log.reference_id

    accounting = request.dbsession.query(PrintAccounting).get(ref)  # type: PrintAccounting
    if accounting is None:
        raise HTTPNotFound("No such ref")
    if "ES_URL" in os.environ:
        logs, total = elastic_search.get_logs(ref, 10000 if debug else 20000, pos, LOG_LIMIT, filter_loggers)
    else:
        logs, total = loki.get_logs(ref, debug, pos, LOG_LIMIT, filter_loggers)
    is_admin = isinstance(request.has_permission("all", {}), Allowed)

    return {
        "ref": ref,
        "debug": debug,
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
        "source": app_id2source(accounting.app_id) if is_admin else None,
    }
