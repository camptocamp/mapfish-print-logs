from datetime import datetime


def test_ok(api_connection, print_job):
    del print_job

    api_connection.login()
    page = api_connection.get("logs/source/simple/accounting")
    print(page)
    now = datetime.now()
    assert f"<td>{now.year}/{now.month:02d}</td>" in page
    assert "<td>0.05</td>" in page


def test_no_login(api_connection):
    r = api_connection.get_raw("logs/source/simple/accounting", expected_status=302, allow_redirects=False)
    assert (
        r.headers["Location"]
        == api_connection.base_url
        + "logs/c2c/github-login?came_from=http%3A%2F%2Fapi%3A8080%2Flogs%2Fsource%2Fsimple%2Faccounting"
    )


def test_csv(api_connection, print_job):
    del print_job

    api_connection.login()
    page = api_connection.get("logs/source/simple/accounting.csv")
    print(page)
    now = datetime.now()
    assert f"month,cost,A4\r\n{now.year}/{now.month:02d},0.05,1\r\n" == page


def test_global_csv(api_connection, print_job):
    del print_job

    api_connection.login()
    page = api_connection.get("logs/accounting.csv")
    print(page)
    now = datetime.now()
    assert f"month,source,cost,A4\r\n{now.year}/{now.month:02d},simple,0.05,1\r\n" == page


def test_global_csv_no_login(api_connection):
    r = api_connection.get_raw("logs/accounting.csv", expected_status=302, allow_redirects=False)
    assert (
        r.headers["Location"]
        == api_connection.base_url
        + "logs/c2c/github-login?came_from=http%3A%2F%2Fapi%3A8080%2Flogs%2Faccounting.csv"
    )
