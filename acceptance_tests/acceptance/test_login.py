def test_ok(api_connection):
    api_connection.login()


def test_kad_key(api_connection):
    r = api_connection.post('logs/login', data=dict(key='bad'))
    assert "<h3>Login</h3>" in r
    assert "Invalid key" in r
