"""Retry behavior of the standalone HTTP helper. No sockets are opened."""

import io
import urllib.error
import urllib.request

import pytest

from unsafe.config import Options, set_options
from unsafe.http import request


class _Scripted:
    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def __call__(self, method, url, data, headers, timeout, proxies):
        self.calls.append(
            {
                "method": method,
                "url": url,
                "data": data,
                "headers": dict(headers),
                "timeout": timeout,
                "proxies": None if proxies is None else dict(proxies),
            }
        )
        outcome = self.results.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        status, body = outcome
        return status, {"Content-Type": "text/plain"}, body


def test_success_does_not_sleep_and_merges_headers():
    transport = _Scripted([(200, b"ok")])
    delays = []
    options = Options(headers={"A": "1", "User-Agent": "custom"}, timeout=4, proxies={"http": "http://127.0.0.1:9"})
    response = request(
        "http://example.test/a",
        headers={"A": "2", "X-Test": "yes"},
        timeout=1.5,
        options=options,
        transport=transport,
        sleeper=delays.append,
    )
    assert response.status == 200
    assert response.text == "ok"
    assert response.json is not None
    assert delays == []
    call = transport.calls[0]
    assert call["headers"]["A"] == "2"
    assert call["headers"]["X-Test"] == "yes"
    assert call["headers"]["User-Agent"] == "custom"
    assert call["timeout"] == 1.5
    assert call["proxies"] == {"http": "http://127.0.0.1:9"}


def test_retry_statuses_use_exponential_backoff_then_return_last_response():
    transport = _Scripted([(500, b"a"), (503, b"b"), (500, b"c")])
    delays = []
    response = request(
        "http://example.test/retry",
        options=Options(max_attempts=3, backoff_factor=0.5),
        transport=transport,
        sleeper=delays.append,
    )
    assert response.status == 500
    assert response.content == b"c"
    assert delays == [0.5, 1.0]
    assert len(transport.calls) == 3


def test_success_after_retry_and_ignored_status():
    transport = _Scripted([(500, b"no"), (200, b"yes")])
    delays = []
    response = request(
        "http://example.test/ok",
        options=Options(max_attempts=3, backoff_factor=0.25),
        transport=transport,
        sleeper=delays.append,
    )
    assert response.status == 200
    assert response.text == "yes"
    assert delays == [0.25]

    transport = _Scripted([(404, b"missing")])
    delays = []
    response = request(
        "http://example.test/missing",
        transport=transport,
        sleeper=delays.append,
    )
    assert response.status == 404
    assert delays == []
    assert len(transport.calls) == 1


def test_post_is_not_retried_by_default_and_opt_in_can_retry_it():
    transport = _Scripted([(500, b"once")])
    response = request(
        "http://example.test/post",
        method="post",
        data=b"body",
        options=Options(max_attempts=4, backoff_factor=1),
        transport=transport,
        sleeper=lambda delay: (_ for _ in ()).throw(AssertionError(delay)),
    )
    assert response.status == 500
    assert transport.calls[0]["data"] == b"body"
    assert len(transport.calls) == 1

    transport = _Scripted([(500, b"a"), (200, b"b")])
    delays = []
    response = request(
        "http://example.test/post",
        method="POST",
        options=Options(max_attempts=2, backoff_factor=0.1, retry_methods=("POST",)),
        transport=transport,
        sleeper=delays.append,
    )
    assert response.status == 200
    assert delays == [0.1]


def test_connection_errors_retry_then_raise():
    down = urllib.error.URLError("down")
    transport = _Scripted([down, (200, b"back")])
    delays = []
    response = request(
        "http://example.test/down",
        options=Options(max_attempts=2, backoff_factor=0.2),
        transport=transport,
        sleeper=delays.append,
    )
    assert response.content == b"back"
    assert delays == [0.2]

    transport = _Scripted([urllib.error.URLError("down"), TimeoutError("slow")])
    with pytest.raises(TimeoutError):
        request(
            "http://example.test/down",
            options=Options(max_attempts=2, backoff_factor=0),
            transport=transport,
            sleeper=lambda delay: (_ for _ in ()).throw(AssertionError(delay)),
        )


def test_active_options_are_used_when_omitted():
    set_options(Options(max_attempts=2, backoff_factor=0.3, timeout=6))
    transport = _Scripted([(500, b"a"), (200, b"b")])
    delays = []
    response = request("http://example.test/ctx", transport=transport, sleeper=delays.append)
    assert response.status == 200
    assert delays == [0.3]
    assert transport.calls[0]["timeout"] == 6
    assert transport.calls[0]["headers"]["User-Agent"] == "unsafe/1.4.0"


def test_non_bytes_body_and_bad_header_values():
    transport = _Scripted([(200, bytearray(b"ab"))])
    response = request("http://example.test/bin", transport=transport)
    assert response.content == b"ab"
    with pytest.raises(TypeError):
        request("http://example.test/bin", headers={"X": 1}, transport=transport)


def test_http_error_without_headers_or_body(monkeypatch):
    class _Bare(urllib.error.HTTPError):
        def __init__(self):
            self.code = 400
            self.headers = None
            self.fp = None

    class _Opener:
        def open(self, req, timeout=None):
            raise _Bare()

    monkeypatch.setattr(urllib.request, "build_opener", lambda *handlers: _Opener())
    response = request("http://example.test/bare")
    assert response.status == 400
    assert response.content == b""
    assert dict(response.headers) == {}


def test_request_rejects_bad_arguments():
    with pytest.raises(ValueError):
        request("")
    with pytest.raises(ValueError):
        request("http://example.test", method="G3T")
    with pytest.raises(TypeError):
        request("http://example.test", data="text")
    with pytest.raises(ValueError):
        request("http://example.test", timeout=0)


def test_response_json():
    transport = _Scripted([(200, b'{"n": 1}')])
    assert request("http://example.test/json", transport=transport).json() == {"n": 1}


def test_urllib_transport_is_mocked(monkeypatch):
    seen = {}

    class _Response:
        status = 201
        headers = {"Content-Type": "text/plain"}

        def read(self):
            return b"hi"

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    class _Opener:
        def open(self, req, timeout=None):
            seen["url"] = req.full_url
            seen["method"] = req.get_method()
            seen["timeout"] = timeout
            seen["data"] = req.data
            return _Response()

    def build_opener(*handlers):
        seen["proxies"] = handlers[0].proxies
        return _Opener()

    monkeypatch.setattr(urllib.request, "build_opener", build_opener)
    response = request(
        "http://example.test/item",
        data=b"xyz",
        method="PUT",
        options=Options(proxies={"http": "http://127.0.0.1:9"}, timeout=2.5, max_attempts=3),
    )
    assert response.status == 201
    assert response.content == b"hi"
    assert seen["url"] == "http://example.test/item"
    assert seen["method"] == "PUT"
    assert seen["timeout"] == 2.5
    assert seen["data"] == b"xyz"
    assert seen["proxies"] == {"http": "http://127.0.0.1:9"}


def test_urllib_http_error_is_returned_and_retried(monkeypatch):
    calls = {"count": 0}

    def http_error(code):
        return urllib.error.HTTPError(
            "http://example.test/err",
            code,
            "nope",
            {"X-Mark": "1"},
            io.BytesIO(b"body"),
        )

    class _Opener:
        def open(self, req, timeout=None):
            calls["count"] += 1
            raise http_error(404 if calls["count"] == 1 else 500)

    monkeypatch.setattr(urllib.request, "build_opener", lambda *handlers: _Opener())
    delays = []
    missing = request("http://example.test/err", sleeper=delays.append)
    assert missing.status == 404
    assert missing.content == b"body"
    assert missing.headers["X-Mark"] == "1"
    assert delays == []

    calls["count"] = 0

    class _Always500:
        def open(self, req, timeout=None):
            raise http_error(500)

    monkeypatch.setattr(urllib.request, "build_opener", lambda *handlers: _Always500())
    delays = []
    failed = request(
        "http://example.test/err",
        options=Options(max_attempts=3, backoff_factor=0.4),
        sleeper=delays.append,
    )
    assert failed.status == 500
    assert delays == [0.4, 0.8]
