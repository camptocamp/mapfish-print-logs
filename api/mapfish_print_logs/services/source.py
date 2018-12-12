from c2cwsgiutils import services
import sqlalchemy as sa

from . import auth_source, get_config_info
from .. import utils
from ..config import SCM_URL_EXTERNAL, JOB_LIMIT
from ..models import DBSession, PrintAccounting

source_service = services.create("source_auth", "/logs/source/{source}")


@source_service.get(renderer='../templates/source.html.mako')
def get_source(request):
    config, key, source = auth_source(request)
    pos = int(request.params.get('pos', '0'))
    app_id = utils.get_app_id(config, source)
    logs = DBSession.query(PrintAccounting).filter(
        sa.or_(
            PrintAccounting.app_id == app_id,
            PrintAccounting.app_id.like(utils.quote_like(app_id) + ":%")
        )
    ).order_by(PrintAccounting.completion_time.desc()).offset(pos).limit(JOB_LIMIT + 1).all()

    scm_refresh_url = f'{SCM_URL_EXTERNAL}1/refresh/{source}/{key}' \
        if SCM_URL_EXTERNAL is not None else None

    return {
        'source': source,
        'jobs': [log for log in logs[:JOB_LIMIT]],
        'scm_refresh_url': scm_refresh_url,
        'config': get_config_info(source, key),
        'next_pos': None if len(logs) <= JOB_LIMIT else pos + JOB_LIMIT,
        'prev_pos': None if pos == 0 else max(0, pos - JOB_LIMIT)
    }
