from pyramid.httpexceptions import HTTPInternalServerError
import requests

from .config import ES_URL, ES_INDEXES, ES_AUTH, ES_FILTERS


def get_logs(ref, min_level):
    if ES_URL is None:
        return []
    query = {
        'size': 5000,
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
        }]
    }
    for filter in ES_FILTERS.split(","):
        name, value = filter.split("=")
        query['query']['bool']['must'].append({
            'term': {name: value}
        })

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json"
    }
    if ES_AUTH is not None:
        headers['Authorization'] = ES_AUTH

    r = requests.post(f"{ES_URL}{ES_INDEXES}/_search", json=query,
                      headers=headers)
    if r.status_code != 200:
        raise HTTPInternalServerError(r.text)
    json = r.json()
    hits = json['hits']['hits']
    return [hit['_source'] for hit in hits]
