import logging

import pytest
from c2cwsgiutils.acceptance import utils
from c2cwsgiutils.acceptance.connection import Connection
from c2cwsgiutils.acceptance.print import PrintConnection

from .fake_print_logs import gen_fake_print_logs

API_URL = "http://api:8080/"
PRINT_URL = "http://print:8080/print"
ES_URL = "http://elasticsearch:9200/elasticsearch"
LOG = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def wait():
    utils.wait_url(API_URL + "logs/c2c/health_check?secret=toto")


class MyConnection(Connection):
    def login(self, key="toto"):
        r = self.session.post(
            self.base_url + "logs/login",
            headers=self._merge_headers({}, True),
            data=dict(key=key),
            allow_redirects=False,
        )
        assert r.status_code == 302
        assert r.headers["Location"] == self.base_url + "logs/"

    def logout(self):
        self.get_raw("logs/logout", expected_status=302, allow_redirects=False)


@pytest.fixture
def api_connection(wait):
    del wait
    return MyConnection(base_url=API_URL, origin="http://example.com/")


@pytest.fixture(scope="session")
def print_connection(wait):
    del wait
    connection = PrintLogConnection(PRINT_URL, PRINT_URL)
    connection.wait_ready()
    return connection


@pytest.fixture(scope="session")
def print_job(print_connection):
    return print_connection.print()


class PrintLogConnection(PrintConnection):
    def print(self):
        examples = self.get_example_requests("simple")
        report = self.get_pdf("simple", examples["requestData"])
        ref = report.url.split("/")[-1]
        gen_fake_print_logs(ref, es_url=ES_URL)
        return ref
