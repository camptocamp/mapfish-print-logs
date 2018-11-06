import urllib.parse


def test_ok(api_connection, print_job):
    page = api_connection.post('logs/source', data=dict(source='simple', key='toto'))
    print(page)
    assert urllib.parse.quote_plus(print_job) in page


def test_get(api_connection, print_job):
    page = api_connection.get('logs/source/simple/toto')
    print(page)
    assert urllib.parse.quote_plus(print_job) in page


def test_bad_key(api_connection):
    api_connection.post('logs/source', data=dict(source='simple', key='bad'), expected_status=403)
