"""Small HTTP client with configurable retry.

The retry loop lives here and is not called by the brute-force, exploit,
crawler, proxy, or vulnerability-scanner modules. By default only idempotent
methods (GET, HEAD, OPTIONS) are retried.
"""

from __future__ import annotations

import logging
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Dict, Mapping, Optional, Tuple

from pydantic import BaseModel, ConfigDict, model_validator

from .__version__ import __version__
from .config import Options, get_options

logger = logging.getLogger("unsafe.http")

_Transport = Callable[
    [str, str, Optional[bytes], Mapping[str, str], float, Optional[Mapping[str, str]]],
    Tuple[int, Mapping[str, str], bytes],
]
_Sleeper = Callable[[float], None]


class Response(BaseModel):
    """Completed HTTP response.

    A retryable status is still returned after the last attempt. ``content``
    is the raw body. ``text`` is that body decoded as UTF-8. ``model_dump``
    includes both; in JSON, ``content`` is base64.
    """

    model_config = ConfigDict(frozen=True)

    status: int
    headers: Dict[str, str]
    url: str
    content: bytes
    text: str = ""

    @model_validator(mode="before")
    @classmethod
    def _decode_text(cls, value: object) -> object:
        if not isinstance(value, dict) or "text" in value or "content" not in value:
            return value
        content = value["content"]
        if not isinstance(content, bytes):
            return value
        decoded = dict(value)
        decoded["text"] = content.decode("utf-8", errors="replace")
        return decoded

    def json_body(self) -> Any:
        """Parse the body as JSON."""
        import json

        return json.loads(self.text)


def request(
    url: str,
    method: str = "GET",
    *,
    data: Optional[bytes] = None,
    headers: Optional[Mapping[str, str]] = None,
    timeout: Optional[float] = None,
    options: Optional[Options] = None,
    transport: Optional[_Transport] = None,
    sleeper: _Sleeper = time.sleep,
) -> Response:
    """Perform one HTTP request, retrying when the active options say so.

    ``max_attempts`` counts the first try. The delay before retry number ``n``
    (starting at 1) is ``backoff_factor * 2 ** (n - 1)``. Connection failures
    and statuses listed in ``retry_statuses`` are retried only when ``method``
    is in ``retry_methods``. A finished HTTP response is returned even when its
    status is still in that list after the final attempt. Connection errors
    are raised after the final attempt.

    Proxies come only from ``options.proxies``. Environment proxy variables are
    not consulted. Per-call ``headers`` override option headers of the same name.
    """
    if not isinstance(url, str) or not url:
        raise ValueError("url must be a non-empty string")
    opts = options if options is not None else get_options()
    verb = method.upper()
    if not verb.isalpha():
        raise ValueError("method must be an HTTP method name")

    merged: Dict[str, str] = dict(opts.headers)
    if headers:
        for key, value in headers.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise TypeError("headers must be a mapping of str to str")
            merged[key] = value
    merged.setdefault("User-Agent", f"unsafe/{__version__}")

    limit = opts.timeout if timeout is None else timeout
    if isinstance(limit, bool) or not isinstance(limit, (int, float)) or limit <= 0:
        raise ValueError("timeout must be a positive number")

    attempts = opts.max_attempts if verb in opts.retry_methods else 1
    send = transport or _urllib_transport
    payload = _payload(data)
    last_error: Optional[BaseException] = None

    for attempt in range(1, attempts + 1):
        try:
            status, resp_headers, body = send(
                verb, url, payload, merged, float(limit), opts.proxies
            )
        except urllib.error.HTTPError as exc:
            status = int(exc.code)
            resp_headers = _header_map(exc.headers)
            body = exc.read() if exc.fp is not None else b""
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            logger.info("%s %s connection failed on attempt %s/%s", verb, url, attempt, attempts)
            if attempt >= attempts:
                raise
            _pause(opts, attempt, sleeper)
            continue

        logger.info("%s %s -> %s (attempt %s/%s)", verb, url, status, attempt, attempts)
        if status in opts.retry_statuses and attempt < attempts:
            _pause(opts, attempt, sleeper)
            continue
        return Response(
            status=int(status),
            headers=dict(resp_headers),
            url=url,
            content=body if isinstance(body, bytes) else bytes(body),
        )

    if last_error is None:
        raise RuntimeError("HTTP request ended without a response or error")
    raise last_error


def _payload(data: Optional[bytes]) -> Optional[bytes]:
    if data is None:
        return None
    if isinstance(data, bytes):
        return data
    raise TypeError("data must be bytes or None")


def _pause(options: Options, attempt: int, sleeper: _Sleeper) -> None:
    delay = options.backoff_factor * (2 ** (attempt - 1))
    if delay > 0:
        sleeper(delay)


def _header_map(headers: object) -> Dict[str, str]:
    if not headers:
        return {}
    items = getattr(headers, "items", None)
    if not callable(items):
        return {}
    raw = items()
    if not isinstance(raw, list) and not hasattr(raw, "__iter__"):
        return {}
    return {str(key): str(value) for key, value in raw}


def _urllib_transport(
    method: str,
    url: str,
    data: Optional[bytes],
    headers: Mapping[str, str],
    timeout: float,
    proxies: Optional[Mapping[str, str]],
) -> Tuple[int, Mapping[str, str], bytes]:
    handler = urllib.request.ProxyHandler(dict(proxies) if proxies else {})
    opener = urllib.request.build_opener(handler)
    req = urllib.request.Request(url, data=data, headers=dict(headers), method=method)
    with opener.open(req, timeout=timeout) as response:
        body = response.read()
        if not isinstance(body, bytes):
            body = bytes(body)
        return int(response.status), _header_map(response.headers), body
