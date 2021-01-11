import c2cwsgiutils.acceptance.connection


def test_ok(api_connection):
    api_connection.get_json(
        "logs/c2c/health_check",
        params=dict(max_level=100),
        cors=False,
        cache_expected=c2cwsgiutils.acceptance.connection.CacheExpected.DONT_CARE,
    )
