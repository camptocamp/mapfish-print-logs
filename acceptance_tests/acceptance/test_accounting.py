from datetime import datetime


def test_ok(api_connection, print_job):
    page = api_connection.post('logs/source/accounting', data=dict(source='simple', key='toto'))
    print(page)
    now = datetime.now()
    assert f'<td>{now.year}/{now.month}</td>' in page
    assert '<td>0.05</td>' in page


def test_bad_key(api_connection):
    api_connection.post('logs/source/accounting', data=dict(source='simple', key='bad'), expected_status=403)


def test_csv(api_connection, print_job):
    page = api_connection.post('logs/source/accounting.csv', data=dict(source='simple', key='toto'))
    print(page)
    now = datetime.now()
    assert f'month,cost,A4\r\n{now.year}/{now.month},0.05,1\r\n' == page


def test_global_csv(api_connection, print_job):
    page = api_connection.post('logs/accounting.csv', data=dict(key='toto'))
    print(page)
    now = datetime.now()
    assert f'month,source,cost,A4\r\n{now.year}/{now.month},simple,0.05,1\r\n' == page
