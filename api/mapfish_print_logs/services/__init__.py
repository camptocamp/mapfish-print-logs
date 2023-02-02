import logging
from typing import Any, Dict, Optional, cast

import requests

from mapfish_print_logs.config import SCM_URL

LOG = logging.getLogger(__name__)


def get_config_info(source: str) -> Optional[Dict[str, Any]]:
    if SCM_URL is None:
        return None
    url = f"{SCM_URL}1/status/{source}"
    try:
        response = requests.get(url)
    except Exception:  # pylint: disable=broad-except
        LOG.exception("Error in request: %s", url)
        return {"status": 500, "message": "Error in sub-request, see logs for details"}
    if response.status_code != 200:
        return {"status": response.status_code, "message": response.text}
    return cast(Dict[str, Any], response.json())
