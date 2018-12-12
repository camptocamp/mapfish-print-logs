import urllib.parse


def test_ok(api_connection, print_job):
    api_connection.login()
    page = api_connection.get('logs/source/simple')
    print(page)
    assert urllib.parse.quote_plus(print_job) in page


def test_no_login(api_connection):
    r = api_connection.get_raw('logs/source/simple', expected_status=302, allow_redirects=False)
    assert r.headers['Location'] == api_connection.base_url + \
        'logs/login?back=/logs/source/simple'
