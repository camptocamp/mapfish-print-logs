from pyramid.httpexceptions import HTTPInternalServerError
import requests

from .config import ES_URL, ES_INDEXES, ES_AUTH


def get_logs(ref):
    if ES_URL is None:
        return []
    query = {
        'size': 1000,
        'query': {
            "bool": {
                "must": [{
                    "match_phrase": {
                        "job_id": ref
                    }
                }]
            }
        },
        'sort': [{
            '@timestamp': {'order': 'asc'}
        }]
    }

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
