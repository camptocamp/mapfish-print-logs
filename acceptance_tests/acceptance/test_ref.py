# we have three non-debug logs and a LOG_LIMIT of 2 => two pages


def test_ok_page1(api_connection, print_job):
    page = api_connection.get('logs/ref', params=dict(ref=print_job))
    print(page)
    assert print_job in page
    assert f'Starting job {print_job}' in page
    assert "DEBUG" not in page
    assert page.count('<tr class="level-') == 2


def test_ok_page2(api_connection, print_job):
    page = api_connection.get('logs/ref', params=dict(ref=print_job, pos=2))
    print(page)
    assert print_job in page
    assert f'Finished job {print_job}' in page
    assert "DEBUG" not in page
    assert page.count('<tr class="level-') == 1


def test_unknown(api_connection):
    api_connection.get('logs/ref', params=dict(ref='unknown'), expected_status=404)


def test_filter(api_connection, print_job):
    page = api_connection.get('logs/ref', params=dict(ref=print_job, filter_loggers='org.mapfish.print',
                                                      min_level='10000'))
    print(page)
    assert print_job in page
    assert f'Starting job {print_job}' not in page
    assert 'Some &lt;b&gt;debug&lt;/b&gt;' in page
