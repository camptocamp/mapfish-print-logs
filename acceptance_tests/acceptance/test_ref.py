def test_ok(api_connection, print_job):
    page = api_connection.get('logs/ref', params=dict(ref=print_job))
    assert print_job in page
