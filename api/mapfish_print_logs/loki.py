import logging
from typing import Dict, List, Tuple, Union

import requests
from pyramid.httpexceptions import HTTPInternalServerError  # type: ignore

from mapfish_print_logs.config import LOKI_AUTH, LOKI_FILTERS, LOKI_URL

SEARCH_HEADERS = {"Content-Type": "application/json;charset=UTF-8", "Accept": "application/json"}
if LOKI_AUTH is not None:
    SEARCH_HEADERS["Authorization"] = LOKI_AUTH

SEARCH_URL = f"{LOKI_URL}loki/api/v1/query_range"

_LOG = logging.getLogger(__name__)


def get_logs(
    ref: str, min_level: int, pos: int, limit: int, filter_loggers: List[str]
) -> Tuple[List[str], int]:
    if LOKI_URL is None:
        return [], 0
    log_query = [f'json.job_id="{ref}"', f"json.level_value>={min_level}"]

    if LOKI_FILTERS != "":
        log_query.append(LOKI_FILTERS)
    if filter_loggers:
        log_query.append(f'json.logger_name=~"{"|".join(filter_loggers)}"')

    _LOG.error(log_query)
    params: Dict[str, Union[str, int]] = {
        "start": pos,
        "limit": limit,
        "query": f"{{{','.join(log_query)}}}",
    }
    _LOG.error(params)
    response = requests.get(
        SEARCH_URL,
        params=params,
        headers=SEARCH_HEADERS,
    )
    if response.status_code != 200:
        raise HTTPInternalServerError(response.text)
    json = response.json()
    return json["data"]["result"][0]["values"], json["data"]["stats"]["decompressedLines"]
