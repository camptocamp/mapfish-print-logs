import requests

ES_URL = 'https://saccas.logs.camptocamp.net/elasticsearch/'
INDEXES = 'saccas-logstash-*'
AUTH = "Basic cHZhbHNlY2NoaTpGb29sMWFyZg=="


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

    r = requests.post(f"{ES_URL}/{INDEXES}/_search", json=query,
                      headers={
                          "Authorization": AUTH,
                          "Content-Type": "application/json;charset=UTF-8",
                          "Accept": "application/json"
                      })
    r.raise_for_status()
    json = r.json()
    hits = json['hits']['hits']
    return [hit['_source'] for hit in hits]


def main():
    logs = get_logs("1e547601-8271-48e6-ac46-1f5104825c36@" +
                    "571479db-cca8-4091-9293-464132b7d2ea@80B34204:C6EC_5BAE0523_2F28:0061")
    for msg in logs:
        print(f"{msg['@timestamp']} [{msg['level_name']}] {msg['logger_name']} - {msg['msg']}")


main()
