from pyramid.httpexceptions import HTTPInternalServerError
import requests

from .config import ES_URL, ES_INDEXES, ES_AUTH, ES_FILTERS

SEARCH_HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json"
}
if ES_AUTH is not None:
    SEARCH_HEADERS['Authorization'] = ES_AUTH

SEARCH_URL = f"{ES_URL}{ES_INDEXES}/_search"


def get_logs(ref, min_level, pos, limit):
    if ES_URL is None:
        return []
    query = {
        'size': limit,
        'from': pos,
        'query': {
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            "job_id": ref
                        }
                    }, {
                        "range": {
                            "level_value": {
                                "gte": min_level
                            }
                        }
                    }
                ]
            }
        },
        'sort': [{
            '@timestamp': {'order': 'asc'}
        }, {
            'offset': {'order': 'asc'}
        }]
    }
    if ES_FILTERS != "":
        for filter_ in ES_FILTERS.split(","):
            name, value = filter_.split("=")
            query['query']['bool']['must'].append({
                'term': {name: value}
            })

    r = requests.post(SEARCH_URL, json=query, headers=SEARCH_HEADERS)
    if r.status_code != 200:
        raise HTTPInternalServerError(r.text)
    json = r.json()
    total = json['hits']['total']
    hits = json['hits']['hits']
    return [hit['_source'] for hit in hits], total
