import os
from typing import Optional


def _ensure_slash(txt: Optional[str]):
    if txt is None:
        return None
    if txt.endswith('/'):
        return txt
    return txt + '/'


JOB_LIMIT = int(os.environ.get('JOB_LIMIT', 10))
LOG_LIMIT = int(os.environ.get('LOG_LIMIT', 300))
SHARED_CONFIG_MASTER = os.environ['SHARED_CONFIG_MASTER']
SCM_URL = _ensure_slash(os.environ.get('SCM_URL'))
SCM_URL_EXTERNAL = _ensure_slash(os.environ.get('SCM_URL_EXTERNAL'))

ES_URL = _ensure_slash(os.environ.get('ES_URL'))
ES_INDEXES = os.environ['ES_INDEXES']
ES_AUTH = os.environ.get('ES_AUTH')
ES_FILTERS = os.environ.get('ES_FILTERS', '')
