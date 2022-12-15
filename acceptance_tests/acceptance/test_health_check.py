def test_ok(api_connection_loki):
    api_connection_loki.get_json("logs/c2c/health_check", params={"max_level": 100})
