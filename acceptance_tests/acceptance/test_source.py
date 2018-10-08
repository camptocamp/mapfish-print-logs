import urllib.parse


def test_ok(api_connection, print_job):
    page = api_connection.post('logs/source', data=dict(source='simple', key='toto'))
    print(page)
    assert urllib.parse.quote_plus(print_job) in page
