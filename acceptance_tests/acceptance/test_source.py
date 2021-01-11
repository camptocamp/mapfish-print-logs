import urllib.parse

import c2cwsgiutils.acceptance.connection


def test_ok(api_connection, print_job):
    api_connection.login()
    page = api_connection.get("logs/source/simple")
    print(page)
    assert urllib.parse.quote_plus(print_job) in page


def test_only_errors(api_connection, print_job):
    api_connection.login()
    page = api_connection.get("logs/source/simple?only_errors=1")
    print(page)
    assert urllib.parse.quote_plus(print_job) not in page


def test_no_login(api_connection):
    r = api_connection.get_raw(
        "logs/source/simple",
        expected_status=302,
        allow_redirects=False,
        cache_expected=c2cwsgiutils.acceptance.connection.CacheExpected.DONT_CARE,
    )
    assert r.headers["Location"] == api_connection.base_url + "logs/login?back=/logs/source/simple"
