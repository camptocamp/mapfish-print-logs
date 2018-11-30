def test_ok(api_connection):
    page = api_connection.post('logs/sources', data=dict(key='toto'))
    print(page)
    assert "simple" in page


def test_bad_key(api_connection):
    api_connection.post('logs/sources', data=dict(key='tutu'), expected_status=403)
