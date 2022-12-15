import functools
import json
import logging
import os
import time
from typing import Any, Callable, Dict, Mapping, Optional

import jwt
import pytest
import requests
from c2cwsgiutils.acceptance import connection, utils

from .fake_print_logs import gen_fake_print_logs_es, gen_fake_print_logs_loki

API_ES_URL = "http://api_es:8080/"
API_LOKI_URL = "http://api_loki:8080/"
PRINT_URL = "http://print:8080/print"
ES_URL = "http://elasticsearch:9200/elasticsearch"
LOKI_URL = "http://loki:3100/"
LOG = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def wait_es():
    utils.wait_url(API_ES_URL + "logs/c2c/health_check?secret=toto")


@pytest.fixture(scope="session")
def wait_loki():
    utils.wait_url(API_LOKI_URL + "logs/c2c/health_check?secret=toto")


class Connection:
    """The connection."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        if not self.base_url.endswith("/"):
            self.base_url += "/"
        self.session = requests.session()

    def get(
        self,
        url: str,
        expected_status: int = 200,
        headers: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> Optional[str]:
        """Get the given URL (relative to the root of API)."""
        r = self.session.get(
            self.base_url + url, headers=dict(headers) if headers is not None else {}, **kwargs
        )
        connection.check_response(r, expected_status)
        return None if r.status_code == 204 else r.text

    def get_raw(
        self,
        url: str,
        expected_status: int = 200,
        headers: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Get the given URL (relative to the root of API)."""
        r = self.session.get(
            self.base_url + url, headers=dict(headers) if headers is not None else {}, **kwargs
        )
        connection.check_response(r, expected_status)
        return r

    def get_json(
        self,
        url: str,
        expected_status: int = 200,
        headers: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> Any:
        """Get the given URL (relative to the root of API)."""
        r = self.session.get(
            self.base_url + url, headers=dict(headers) if headers is not None else {}, **kwargs
        )
        connection.check_response(r, expected_status)
        return r.json()

    def post(
        self,
        url: str,
        expected_status: int = 200,
        headers: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> Optional[str]:
        """POST the given URL (relative to the root of API)."""
        r = self.session.post(
            self.base_url + url, headers=dict(headers) if headers is not None else {}, **kwargs
        )
        connection.check_response(r, expected_status)
        return None if r.status_code == 204 else r.text

    def post_json(
        self,
        url: str,
        expected_status: int = 200,
        headers: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> Any:
        """POST the given URL (relative to the root of API)."""
        r = self.session.post(
            self.base_url + url, headers=dict(headers) if headers is not None else {}, **kwargs
        )
        connection.check_response(r, expected_status)
        return r.json()

    def delete(
        self,
        url: str,
        expected_status: int = 204,
        headers: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """DELETE the given URL (relative to the root of API)."""
        r = self.session.delete(
            self.base_url + url, headers=dict(headers) if headers is not None else {}, **kwargs
        )
        connection.check_response(r, expected_status)
        return r


class PrintConnection(Connection):
    """A Connection with specialized methods to interact with a MapFish Print server."""

    def __init__(self, base_url: str) -> None:
        """
        Initialize.

        Arguments:
            base_url: The base URL to the print server (including the /print)
        """
        super().__init__(base_url=base_url)

    def wait_ready(self, timeout: int = 60, app: str = "default") -> None:
        """Wait the print instance to be ready."""
        retry_timeout(functools.partial(self.get_capabilities, app=app), timeout=timeout)

    def get_capabilities(self, app: str) -> Any:
        return self.get_json(app + "/capabilities.json")

    def get_example_requests(self, app: str) -> Dict[str, Any]:
        samples = self.get_json(app + "/exampleRequest.json")
        out = {}
        for name, value in samples.items():
            out[name] = json.loads(value)
        return out

    def get_pdf(self, app: str, request: Dict[str, Any], timeout: int = 60) -> requests.Response:
        create_report = self.post_json(app + "/report.pdf", json=request)
        LOG.debug("create_report=%s", create_report)
        ref = create_report["ref"]

        status = retry_timeout(functools.partial(self._check_completion, ref), timeout=timeout)
        LOG.debug("status=%s", repr(status))
        assert status["status"] == "finished"

        report = self.get_raw("report/" + ref)
        assert report.headers["Content-Type"] == "application/pdf"
        return report

    def _check_completion(self, ref: str) -> Optional[Any]:
        status = self.get_json(f"status/{ref}.json")
        if status["done"]:
            return status
        return None

    def get_apps(self) -> Any:
        return self.get_json("apps.json")


class PrintLogConnectionES(PrintConnection):
    def print(self):
        examples = self.get_example_requests("simple")
        report = self.get_pdf("simple", examples["requestData"])
        ref = report.url.split("/")[-1]
        gen_fake_print_logs_es(ref, es_url=ES_URL)
        return ref


class PrintLogConnectionLoki(PrintConnection):
    def print(self):
        utils.wait_url(LOKI_URL + "/ready")

        examples = self.get_example_requests("simple")
        report = self.get_pdf("simple", examples["requestData"])
        ref = report.url.split("/")[-1]
        gen_fake_print_logs_loki(ref, loki_url=LOKI_URL)
        return ref


class MyConnection(Connection):
    def login(self):
        self.session.cookies["c2c-auth-jwt"] = jwt.encode(
            {
                "login": "testlogin",
                "name": "Test user",
                "url": "http://example.com",
                "token": {"access_token": os.environ["GITHUB_TOKEN"]},
            },
            "a-secret-long-a-secret",
            algorithm="HS256",
        )

    def logout(self):
        if "c2c-auth-jwt" in self.session.cookies:
            del self.session.cookies["c2c-auth-jwt"]


@pytest.fixture
def api_connection_es(wait):
    del wait
    return MyConnection(base_url=API_ES_URL)


@pytest.fixture
def api_connection_loki(wait):
    del wait
    return MyConnection(base_url=API_LOKI_URL)


@pytest.fixture(scope="session")
def print_connection_es(wait):
    del wait
    connection = PrintLogConnectionES(PRINT_URL)
    connection.wait_ready()
    return connection


@pytest.fixture(scope="session")
def print_connection_loki(wait):
    del wait
    connection = PrintLogConnectionLoki(PRINT_URL)
    connection.wait_ready()
    return connection


@pytest.fixture_es(scope="session")
def print_job(print_connection_es):
    return print_connection_es.print()


@pytest.fixture(scope="session")
def print_job_loki(print_connection_loki):
    return print_connection_loki.print()


def retry_timeout(what: Callable[[], Any], timeout: float = 60, interval: float = 0.5) -> Any:
    """
    Retry the function until the timeout.

    Arguments:

        what: the function to try
        timeout: the timeout to get a success
        interval: the interval between try
    """
    timeout = time.monotonic() + timeout
    while True:
        error = ""
        try:
            ret = what()
            if ret:
                return ret
        except KeyError:
            raise
        except NameError:
            raise
        except Exception as e:  # pylint: disable=broad-except
            error = e
            LOG.exception("== Failed ==")
        if time.monotonic() > timeout:
            assert False, f"Timeout: {type(error)}: {str(error)}"
        time.sleep(interval)
