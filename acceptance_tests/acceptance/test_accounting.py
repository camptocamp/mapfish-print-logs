from datetime import datetime


def test_ok(api_connection_loki, print_job_loki):
    del print_job_loki

    api_connection_loki.login()
    page = api_connection_loki.get("logs/source/simple/accounting")
    print(page)
    now = datetime.now()
    assert f"<td>{now.year}/{now.month:02d}</td>" in page
    assert "<td>0.05</td>" in page


def test_no_login(api_connection_loki):
    r = api_connection_loki.get_raw(
        "logs/source/simple/accounting", expected_status=302, allow_redirects=False
    )
    assert (
        r.headers["Location"]
        == api_connection_loki.base_url
        + "logs/c2c/github-login?came_from=http%3A%2F%2Fapi%3A8080%2Flogs%2Fsource%2Fsimple%2Faccounting"
    )


def test_csv(api_connection_loki, print_job_loki):
    del print_job_loki

    api_connection_loki.login()
    page = api_connection_loki.get("logs/source/simple/accounting.csv")
    print(page)
    now = datetime.now()
    assert f"month,cost,A4\r\n{now.year}/{now.month:02d},0.05,1\r\n" == page


def test_global_csv(api_connection_loki, print_job_loki):
    del print_job_loki

    api_connection_loki.login()
    page = api_connection_loki.get("logs/accounting.csv")
    print(page)
    now = datetime.now()
    assert f"month,source,cost,A4\r\n{now.year}/{now.month:02d},simple,0.05,1\r\n" == page


def test_global_csv_no_login(api_connection_loki):
    r = api_connection_loki.get_raw("logs/accounting.csv", expected_status=302, allow_redirects=False)
    assert (
        r.headers["Location"]
        == api_connection_loki.base_url
        + "logs/c2c/github-login?came_from=http%3A%2F%2Fapi%3A8080%2Flogs%2Faccounting.csv"
    )
