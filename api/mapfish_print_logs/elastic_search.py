import os
from pyramid.httpexceptions import HTTPInternalServerError
import requests

ES_URL = os.environ['ES_URL']
INDEXES = os.environ['ES_INDEXES']
AUTH = os.environ.get('ES_AUTH')


def get_logs(ref):
    query = {
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


def main():
    logs = get_logs("1e547601-8271-48e6-ac46-1f5104825c36@" +
                    "571479db-cca8-4091-9293-464132b7d2ea@80B34204:C6EC_5BAE0523_2F28:0061")
    for msg in logs:
        print(f"{msg['@timestamp']} [{msg['level_name']}] {msg['logger_name']} - {msg['msg']}")


main()
