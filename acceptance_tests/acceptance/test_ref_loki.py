# we have three non-debug logs and a LOG_LIMIT of 2 => two pages


def test_ok_page1(api_connection_loki, print_job_loki):
    page = api_connection_loki.get("logs/ref", params={"ref": print_job_loki})
    print(page)
    assert print_job_loki in page
    assert f"Starting job {print_job_loki}" in page
    assert "DEBUG" not in page
    assert page.count('<tr class="level-') == 3


def test_ok_page2(api_connection_loki, print_job_loki):
    page = api_connection_loki.get("logs/ref", params={"ref": print_job_loki, "pos": 2})
    print(page)
    assert print_job_loki in page
    assert f"Finished job {print_job_loki}" in page
    assert "DEBUG" not in page
    assert page.count('<tr class="level-') == 1


def test_unknown(api_connection_loki):
    api_connection_loki.get("logs/ref", params={"ref": "unknown"}, expected_status=404)


def test_filter(api_connection_loki, print_job_loki):
    page = api_connection_loki.get(
        "logs/ref",
        params={
            "ref": print_job_loki,
            "filter_loggers": "org.mapfish.print",
            "min_level": "10000",
        },
    )
    print(page)
    assert print_job_loki in page
    assert f"Starting job {print_job_loki}" not in page
    assert "Some &lt;b&gt;debug&lt;/b&gt;" in page
