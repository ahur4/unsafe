"""Shared options for timeouts, headers, proxies, and output.

This module is configuration plumbing. No attack, scanner, or brute-force
module reads it.
"""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from contextvars import ContextVar
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

T = TypeVar("T")
R = TypeVar("R")

OutputFormat = Literal["text", "json"]


def _copy_strings(name: str, value: object) -> Dict[str, str]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping of str to str")
    copied: Dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise TypeError(f"{name} must be a mapping of str to str")
        copied[key] = item
    return copied


class Options(BaseModel):
    """Process-wide defaults for the shared HTTP and output helpers.

    The model is frozen and re-validates on :meth:`replace`. ``headers`` and
    ``proxies`` replace the previous mapping; they are not merged. Both are
    copied, so later changes to the dict you passed in are ignored.

    JSON output is ``model_dump_json``. A plain dict is ``model_dump``.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    timeout: float = 10.0
    headers: Dict[str, str] = Field(default_factory=dict)
    proxies: Optional[Dict[str, str]] = None
    concurrency: int = 1
    verbosity: int = 0
    output_format: OutputFormat = "text"
    max_attempts: int = 3
    backoff_factor: float = 0.5
    retry_statuses: Tuple[int, ...] = (429, 500, 502, 503, 504)
    retry_methods: Tuple[str, ...] = ("GET", "HEAD", "OPTIONS")

    @field_validator("timeout", "backoff_factor", mode="before")
    @classmethod
    def _reject_bool_number(cls, value: object) -> object:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("expected a number")
        return value

    @field_validator("timeout")
    @classmethod
    def _positive_timeout(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("timeout must be > 0")
        return float(value)

    @field_validator("backoff_factor")
    @classmethod
    def _non_negative_backoff(cls, value: float) -> float:
        if value < 0:
            raise ValueError("backoff_factor must be >= 0")
        return float(value)

    @field_validator("concurrency", "verbosity", "max_attempts", mode="before")
    @classmethod
    def _reject_bool_int(cls, value: object, info: ValidationInfo) -> object:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{info.field_name} must be an int")
        return value

    @field_validator("concurrency", "max_attempts")
    @classmethod
    def _at_least_one(cls, value: int, info: ValidationInfo) -> int:
        if value < 1:
            raise ValueError(f"{info.field_name} must be >= 1")
        return value

    @field_validator("verbosity")
    @classmethod
    def _non_negative_verbosity(cls, value: int) -> int:
        if value < 0:
            raise ValueError("verbosity must be >= 0")
        return value

    @field_validator("output_format", mode="before")
    @classmethod
    def _normalize_format(cls, value: object) -> object:
        if isinstance(value, str):
            return value.lower()
        return value

    @field_validator("headers", mode="before")
    @classmethod
    def _headers(cls, value: object) -> Dict[str, str]:
        return _copy_strings("headers", value)

    @field_validator("proxies", mode="before")
    @classmethod
    def _proxies(cls, value: object) -> Optional[Dict[str, str]]:
        if value is None:
            return None
        return _copy_strings("proxies", value)

    @field_validator("retry_statuses", mode="before")
    @classmethod
    def _statuses(cls, value: object) -> Tuple[int, ...]:
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise TypeError("retry_statuses must be a sequence of HTTP status codes")
        statuses: List[int] = []
        for status in value:
            if isinstance(status, bool) or not isinstance(status, int):
                raise TypeError("retry_statuses must contain integers")
            if status < 100 or status > 599:
                raise ValueError("retry_statuses must be HTTP status codes")
            statuses.append(status)
        return tuple(statuses)

    @field_validator("retry_methods", mode="before")
    @classmethod
    def _methods(cls, value: object) -> Tuple[str, ...]:
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise TypeError("retry_methods must be a sequence of HTTP method names")
        methods: List[str] = []
        for method in value:
            if not isinstance(method, str) or not method.strip():
                raise TypeError("retry_methods must contain HTTP method names")
            methods.append(method.upper())
        return tuple(methods)

    def replace(self, **overrides: Any) -> "Options":
        """Return a validated copy with ``overrides`` applied."""
        merged = self.model_dump()
        merged.update(overrides)
        return Options.model_validate(merged)


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
    """Format ``value`` as text or JSON using the active output format.

    Pydantic models use :meth:`~pydantic.BaseModel.model_dump_json` for JSON
    and :meth:`~pydantic.BaseModel.model_dump` for text. Other values use
    ``json.dumps`` or ``key: value`` lines.
    """
    from pydantic import BaseModel

    opts = options if options is not None else get_options()
    if isinstance(value, BaseModel):
        if opts.output_format == "json":
            return value.model_dump_json(indent=2)
        payload: Any = value.model_dump()
    else:
        payload = value
    if opts.output_format == "json":
        return json.dumps(payload, default=str, indent=2, sort_keys=True)
    if isinstance(payload, Mapping):
        return "\n".join(f"{key}: {item}" for key, item in payload.items())
    if isinstance(payload, (list, tuple)):
        return "\n".join(str(item) for item in payload)
    return str(payload)


def map_concurrent(
    function: Callable[[T], R],
    items: Sequence[T],
    options: Optional[Options] = None,
) -> List[R]:
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
