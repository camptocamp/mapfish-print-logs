def test_ok(api_connection, print_job):
    page = api_connection.get('logs/ref', params=dict(ref=print_job))
    assert print_job in page


def test_unknown(api_connection):
    api_connection.get('logs/ref', params=dict(ref='unknown'), expected_status=404)
