from typing import Any, Dict, List, Tuple

import requests
from pyramid.httpexceptions import HTTPInternalServerError  # type: ignore

from mapfish_print_logs.config import ES_AUTH, ES_FILTERS, ES_INDEXES, ES_URL

SEARCH_HEADERS = {"Content-Type": "application/json;charset=UTF-8", "Accept": "application/json"}
if ES_AUTH is not None:
    SEARCH_HEADERS["Authorization"] = ES_AUTH

SEARCH_URL = f"{ES_URL}{ES_INDEXES}/_search"


def get_logs(ref: str, min_level: int, pos: int, limit: int, filter_loggers: str) -> Tuple[List[str], int]:
    if ES_URL is None:
        return [], 0
    query: Dict[str, Any] = {
        "size": limit,
        "from": pos,
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"json.job_id": ref}},
                    {"range": {"json.level_value": {"gte": min_level}}},
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "asc"}}, {"log.offset": {"order": "asc", "unmapped_type": "long"}}],
    }
    if ES_FILTERS != "":
        for filter_ in ES_FILTERS.split(","):
            name, value = filter_.split("=")
            query["query"]["bool"]["must"].append({"term": {name: value}})
    if filter_loggers:
        query["query"]["bool"]["must_not"] = [
            {"match_phrase": {"json.logger_name": x}} for x in filter_loggers
        ]

    response = requests.post(SEARCH_URL, json=query, headers=SEARCH_HEADERS)
    if response.status_code != 200:
        raise HTTPInternalServerError(response.text)
    json = response.json()
    total = json["hits"]["total"]["value"]
    hits = json["hits"]["hits"]
    return [hit["_source"] for hit in hits], total
