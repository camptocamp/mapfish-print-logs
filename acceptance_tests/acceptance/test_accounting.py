from datetime import datetime


def test_ok(api_connection, print_job):
    page = api_connection.post('logs/source/accounting', data=dict(source='simple', key='toto'))
    print(page)
    now = datetime.now()
    assert f'<td>{now.year}/{now.month}</td>' in page
    assert '<td>0.05</td>' in page


def test_bad_key(api_connection):
    api_connection.post('logs/source/accounting', data=dict(source='simple', key='bad'), expected_status=403)
