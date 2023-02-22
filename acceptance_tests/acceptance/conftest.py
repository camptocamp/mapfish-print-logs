import functools
import json
import logging

import pytest
from c2cwsgiutils.acceptance import utils
from c2cwsgiutils.acceptance.connection import CacheExpected, Connection, check_response
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

    def get_capabilities(self, app: str):
        return self.get_json(app + "/capabilities.json", cors=False, cache_expected=CacheExpected.DONT_CARE)

    def get_example_requests(self, app: str):
        samples = self.get_json(
            app + "/exampleRequest.json", cors=False, cache_expected=CacheExpected.DONT_CARE
        )
        out = {}
        for name, value in samples.items():
            out[name] = json.loads(value)
        return out

    def get_pdf(self, app: str, request, timeout: int = 60):
        create_report = self.post_json(
            app + "/report.pdf", json=request, cors=False, cache_expected=CacheExpected.DONT_CARE
        )
        LOG.debug("create_report=%s", create_report)
        ref = create_report["ref"]

        status = utils.retry_timeout(functools.partial(self._check_completion, ref), timeout=timeout)
        LOG.debug("status=%s", repr(status))
        assert status["status"] == "finished"

        report = self.get_raw("report/" + ref, cors=False, cache_expected=CacheExpected.DONT_CARE)
        assert report.headers["Content-Type"] == "application/pdf"
        return report

    def _check_completion(self, ref: str):
        status = self.get_json(
            "status/{ref}.json".format(ref=ref), cors=False, cache_expected=CacheExpected.DONT_CARE
        )
        if status["done"]:
            return status
        return None
