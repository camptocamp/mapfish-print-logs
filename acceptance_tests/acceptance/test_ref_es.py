# we have three non-debug logs and a LOG_LIMIT of 2 => two pages


def test_ok_page1(api_connection_es, print_job_es):
    page = api_connection_es.get("logs/ref", params={"ref": print_job_es})
    print(page)
    assert print_job_es in page
    assert f"Starting job {print_job_es}" in page
    assert "DEBUG" not in page
    assert page.count('<tr class="level-') == 3


def test_ok_page2(api_connection_es, print_job_es):
    page = api_connection_es.get("logs/ref", params={"ref": print_job_es, "pos": 2})
    print(page)
    assert print_job_es in page
    assert f"Finished job {print_job_es}" in page
    assert "DEBUG" not in page
    assert page.count('<tr class="level-') == 1


def test_unknown(api_connection_es):
    api_connection_es.get("logs/ref", params={"ref": "unknown"}, expected_status=404)


def test_filter(api_connection_es, print_job_es):
    page = api_connection_es.get(
        "logs/ref",
        params={
            "ref": print_job_es,
            "filter_loggers": "org.mapfish.print",
            "debug": "true",
        },
    )
    print(page)
    assert print_job_es in page
    assert f"Starting job {print_job_es}" not in page
    assert "Some &lt;b&gt;debug&lt;/b&gt;" in page
