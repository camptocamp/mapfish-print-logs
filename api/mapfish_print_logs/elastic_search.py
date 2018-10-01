import os
from pyramid.httpexceptions import HTTPInternalServerError
import requests

ES_URL = os.environ['ES_URL']
INDEXES = os.environ['ES_INDEXES']
AUTH = os.environ.get('ES_AUTH')


def get_logs(ref):
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
    if AUTH is not None:
        headers['Authorization'] = AUTH

    r = requests.post(f"{ES_URL}/{INDEXES}/_search", json=query,
                      headers=headers)
    if r.status_code != 200:
        raise HTTPInternalServerError(r.text)
    json = r.json()
    hits = json['hits']['hits']
    return [hit['_source'] for hit in hits]
