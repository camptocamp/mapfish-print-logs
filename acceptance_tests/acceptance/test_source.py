import urllib.parse


def test_ok(api_connection_loki, print_job_loki):
    api_connection_loki.login()
    page = api_connection_loki.get("logs/source/simple")
    print(page)
    assert urllib.parse.quote_plus(print_job_loki) in page


def test_only_errors(api_connection_loki, print_job_loki):
    api_connection_loki.login()
    page = api_connection_loki.get("logs/source/simple?only_errors=1")
    print(page)
    assert urllib.parse.quote_plus(print_job_loki) not in page


def test_no_login(api_connection_loki):
    r = api_connection_loki.get_raw("logs/source/simple", expected_status=302, allow_redirects=False)
    assert (
        r.headers["Location"]
        == api_connection_loki.base_url
        + "logs/c2c/github-login?came_from=http%3A%2F%2Fapi%3A8080%2Flogs%2Fsource%2Fsimple"
    )
