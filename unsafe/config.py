"""Shared options for timeouts, headers, proxies, and output.

This module is configuration plumbing. No other feature module reads it, so
changing these values does not alter brute-force, exploit, scanner, or bypass
behavior.
"""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import Any, Callable, Dict, Iterator, Mapping, Optional, Sequence, TypeVar

T = TypeVar("T")
R = TypeVar("R")

_TEXT = "text"
_JSON = "json"
_OUTPUT_FORMATS = (_TEXT, _JSON)


def _require_int(name: str, value: int, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


def _require_number(name: str, value: float, minimum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return float(value)


def _string_mapping(name: str, value: Optional[Mapping[str, str]]) -> Optional[Mapping[str, str]]:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping of str to str")
    copied: Dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise TypeError(f"{name} must be a mapping of str to str")
        copied[key] = item
    return MappingProxyType(copied)


@dataclass(frozen=True)
class Options:
    """Process-wide defaults for the shared HTTP and output helpers.

    Mappings are copied and frozen when the object is created. Use
    :meth:`replace` to change a value. ``headers`` and ``proxies`` replace the
    previous mapping; they are not merged.
    """

    timeout: float = 10.0
    headers: Mapping[str, str] = field(default_factory=dict)
    proxies: Optional[Mapping[str, str]] = None
    concurrency: int = 1
    verbosity: int = 0
    output_format: str = _TEXT
    max_attempts: int = 3
    backoff_factor: float = 0.5
    retry_statuses: tuple = (429, 500, 502, 503, 504)
    retry_methods: tuple = ("GET", "HEAD", "OPTIONS")

    def __post_init__(self) -> None:
        timeout = _require_number("timeout", self.timeout, 0)
        if timeout == 0:
            raise ValueError("timeout must be > 0")
        object.__setattr__(self, "timeout", timeout)
        object.__setattr__(self, "concurrency", _require_int("concurrency", self.concurrency, 1))
        object.__setattr__(self, "verbosity", _require_int("verbosity", self.verbosity, 0))
        object.__setattr__(self, "max_attempts", _require_int("max_attempts", self.max_attempts, 1))
        object.__setattr__(
            self, "backoff_factor", _require_number("backoff_factor", self.backoff_factor, 0)
        )

        output_format = str(self.output_format).lower()
        if output_format not in _OUTPUT_FORMATS:
            allowed = ", ".join(_OUTPUT_FORMATS)
            raise ValueError(f"output_format must be one of: {allowed}")
        object.__setattr__(self, "output_format", output_format)

        headers = _string_mapping("headers", self.headers) or MappingProxyType({})
        object.__setattr__(self, "headers", headers)
        object.__setattr__(self, "proxies", _string_mapping("proxies", self.proxies))

        statuses = []
        for status in self.retry_statuses:
            if isinstance(status, bool) or not isinstance(status, int):
                raise TypeError("retry_statuses must contain integers")
            if status < 100 or status > 599:
                raise ValueError("retry_statuses must be HTTP status codes")
            statuses.append(status)
        object.__setattr__(self, "retry_statuses", tuple(statuses))

        methods = []
        for method in self.retry_methods:
            if not isinstance(method, str) or not method.strip():
                raise TypeError("retry_methods must contain HTTP method names")
            methods.append(method.upper())
        object.__setattr__(self, "retry_methods", tuple(methods))

    def replace(self, **overrides: Any) -> "Options":
        """Return a copy with ``overrides`` applied."""
        return replace(self, **overrides)


_CURRENT: ContextVar[Options] = ContextVar("unsafe_options", default=Options())


def get_options() -> Options:
    """Return the options active in this context."""
    return _CURRENT.get()


def set_options(options: Options) -> None:
    """Replace the active options and apply :attr:`Options.verbosity`."""
    if not isinstance(options, Options):
        raise TypeError("options must be an Options instance")
    _CURRENT.set(options)
    apply_verbosity(options)


@contextmanager
def use_options(**overrides: Any) -> Iterator[Options]:
    """Temporarily apply ``overrides`` on top of the active options."""
    updated = get_options().replace(**overrides)
    token = _CURRENT.set(updated)
    apply_verbosity(updated)
    try:
        yield updated
    finally:
        _CURRENT.reset(token)
        apply_verbosity(get_options())


def apply_verbosity(options: Optional[Options] = None) -> None:
    """Set the ``unsafe`` logger level from ``options.verbosity``.

    ``0`` is warning, ``1`` is info, and ``2`` or more is debug. This does not
    attach a handler or change the root logger.
    """
    opts = options if options is not None else get_options()
    if opts.verbosity >= 2:
        level = logging.DEBUG
    elif opts.verbosity == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.getLogger("unsafe").setLevel(level)


def render(value: Any, options: Optional[Options] = None) -> str:
    """Format ``value`` as text or JSON using the active output format."""
    opts = options if options is not None else get_options()
    if opts.output_format == _JSON:
        return json.dumps(value, default=str, indent=2, sort_keys=True)
    if isinstance(value, Mapping):
        return "\n".join(f"{key}: {item}" for key, item in value.items())
    if isinstance(value, (list, tuple)):
        return "\n".join(str(item) for item in value)
    return str(value)


def map_concurrent(
    function: Callable[[T], R],
    items: Sequence[T],
    options: Optional[Options] = None,
) -> list:
    """Apply ``function`` to ``items``, using ``options.concurrency`` workers.

    This is a generic helper. No scanner, finder, or exploit module calls it.
    Results stay in input order. A concurrency of ``1`` runs in the caller.
    """
    opts = options if options is not None else get_options()
    sequence = list(items)
    if opts.concurrency == 1 or len(sequence) <= 1:
        return [function(item) for item in sequence]
    with ThreadPoolExecutor(max_workers=opts.concurrency) as executor:
        return list(executor.map(function, sequence))
