from typing import Any, Dict, Optional, cast

import pyramid.request  # type: ignore
import sqlalchemy as sa  # type: ignore
from c2cwsgiutils import services

from mapfish_print_logs import utils
from mapfish_print_logs.config import JOB_LIMIT, SCM_URL_EXTERNAL
from mapfish_print_logs.models import PrintAccounting
from mapfish_print_logs.security import auth_source
from mapfish_print_logs.services import get_config_info

source_service = services.create("source_auth", "/logs/source/{source}")


@source_service.get(renderer="../templates/source.html.mako")  # type: ignore
def get_source(request: pyramid.request.Request) -> Dict[str, Any]:
    config, source = auth_source(request)
    pos = int(request.params.get("pos", "0"))
    only_errors = request.params.get("only_errors", "0") == "1"
    query = request.dbsession.query(PrintAccounting)
    if source != "all":
        app_id = utils.get_app_id(config, source)
        query = query.filter(
            sa.or_(
                PrintAccounting.app_id == app_id, PrintAccounting.app_id.like(utils.quote_like(app_id) + ":%")
            )
        )
        source_key = config["sources"][source]["key"]
        scm_refresh_url: Optional[str] = (
            f"{SCM_URL_EXTERNAL}1/refresh/{source}/{source_key}" if SCM_URL_EXTERNAL is not None else None
        )
    else:
        source_key = None
        scm_refresh_url = None
    if only_errors:
        query = query.filter(PrintAccounting.status != "FINISHED")
    logs = query.order_by(PrintAccounting.completion_time.desc()).offset(pos).limit(JOB_LIMIT + 1).all()

    return {
        "source": source,
        "jobs": logs[:JOB_LIMIT],
        "scm_refresh_url": scm_refresh_url,
        "config": get_config_info(source, cast(str, source_key)) if source != "all" else None,
        "next_pos": None if len(logs) <= JOB_LIMIT else pos + JOB_LIMIT,
        "prev_pos": None if pos == 0 else max(0, pos - JOB_LIMIT),
        "only_errors": only_errors,
    }
