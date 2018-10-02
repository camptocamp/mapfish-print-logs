def test_ok(api_connection):
    api_connection.get("logs/")


def test_no_slash(api_connection):
    api_connection.get("logs")
