def test_ok(api_connection_loki):
    api_connection_loki.get("logs/")


def test_no_slash(api_connection_loki):
    api_connection_loki.get("logs")
