def test_ok(api_connection):
    api_connection.get_json("logs/c2c/health_check", params=dict(max_level=100), cors=False)
