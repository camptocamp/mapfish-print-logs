import datetime
import os
import requests
import sys

# flake8: noqa: E501


ES_URL = os.environ.get('ES_URL', 'http://localhost:9200/elasticsearch')
INDEX = os.environ.get('ES_INDEX', 'print-1')
OFFSET = 0
LEVEL_VALUE = {
    'DEBUG': 10000,
    'INFO': 20000,
    'WARN': 30000
}


def _log_message(es_url, ref, level, message, **kwargs):
    global OFFSET
    OFFSET += 1
    data = {
        'json': {
            'job_id': ref,
            'level_name': level,
            'level_value': LEVEL_VALUE[level],
            'msg': message,
        },
        '@timestamp': datetime.datetime.now().isoformat(),
        'kubernetes': {
            'labels': {
                'release': 'prod'
            }
        },
        'log': {
            'offset': OFFSET
        }
    }
    data['json'].update(kwargs)
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json"
    }
    r = requests.post(f"{es_url}/{INDEX}?refresh=wait_for", json=data,
                      headers=headers)
    r.raise_for_status()


def gen_fake_print_logs(ref, es_url=ES_URL):
    _log_message(es_url, ref, 'INFO', f'Starting job {ref}', logger_name="org.mapfish.print")
    _log_message(es_url, ref, 'DEBUG', f'Some <b>debug</b>', logger_name="org.mapfish.print.map")
    _log_message(es_url, ref, 'WARN', f'Some warning with stacktrace', logger_name="unknown.jul.logger",
                 thread_name="Post result to registry", stack_trace="""\
java.net.SocketTimeoutException: connect timed out
    at java.net.PlainSocketImpl.socketConnect(Native Method)
    at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
    at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
    at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
    at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
    at java.net.Socket.connect(Socket.java:589)
    at org.postgresql.core.PGStream.<init>(PGStream.java:69)
    at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:156)
    at org.postgresql.core.ConnectionFactory.openConnection(ConnectionFactory.java:49)
    at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:195)
    at org.postgresql.Driver.makeConnection(Driver.java:452)
    at org.postgresql.Driver.connect(Driver.java:254)
    at java.sql.DriverManager.getConnection(DriverManager.java:664)
    at java.sql.DriverManager.getConnection(DriverManager.java:208)
    at org.springframework.jdbc.datasource.DriverManagerDataSource.getConnectionFromDriverManager(DriverManagerDataSource.java:153)
    at org.springframework.jdbc.datasource.DriverManagerDataSource.getConnectionFromDriver(DriverManagerDataSource.java:144)
    at org.springframework.jdbc.datasource.AbstractDriverBasedDataSource.getConnectionFromDriver(AbstractDriverBasedDataSource.java:196)
    at org.springframework.jdbc.datasource.AbstractDriverBasedDataSource.getConnection(AbstractDriverBasedDataSource.java:159)
    at org.hibernate.engine.jdbc.connections.internal.DatasourceConnectionProviderImpl.getConnection(DatasourceConnectionProviderImpl.java:139)
    at org.hibernate.internal.AbstractSessionImpl$NonContextualJdbcConnectionAccess.obtainConnection(AbstractSessionImpl.java:380)
    at org.hibernate.engine.jdbc.internal.LogicalConnectionImpl.obtainConnection(LogicalConnectionImpl.java:228)
    at org.hibernate.engine.jdbc.internal.LogicalConnectionImpl.getConnection(LogicalConnectionImpl.java:171)
    at org.hibernate.internal.SessionImpl.connection(SessionImpl.java:450)
    at org.springframework.orm.hibernate4.HibernateTransactionManager.doBegin(HibernateTransactionManager.java:450)
    at org.springframework.transaction.support.AbstractPlatformTransactionManager.getTransaction(AbstractPlatformTransactionManager.java:377)
    at org.springframework.transaction.interceptor.TransactionAspectSupport.createTransactionIfNecessary(TransactionAspectSupport.java:461)
    at org.springframework.transaction.interceptor.TransactionAspectSupport.invokeWithinTransaction(TransactionAspectSupport.java:277)
    at org.springframework.transaction.interceptor.TransactionInterceptor.invoke(TransactionInterceptor.java:96)
    at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:179)
    at org.springframework.aop.framework.JdkDynamicAopProxy.invoke(JdkDynamicAopProxy.java:213)
    at com.sun.proxy.$Proxy33.toCancel(Unknown Source)
    at org.mapfish.print.servlet.job.impl.ThreadPoolJobManager.pollRegistry(ThreadPoolJobManager.java:443)
    at org.mapfish.print.servlet.job.impl.ThreadPoolJobManager.access$800(ThreadPoolJobManager.java:46)
    at org.mapfish.print.servlet.job.impl.ThreadPoolJobManager$RegistryTask.run(ThreadPoolJobManager.java:424)
    at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
    at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308)
    at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180)
    at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294)
    at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
    at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
    at java.lang.Thread.run(Thread.java:748)
""")
    _log_message(es_url, ref, 'INFO', f'Finished job {ref} with some very long message', logger_name="org.mapfish.print")


def main():
    gen_fake_print_logs(sys.argv[1])


if __name__ == '__main__':
    main()
