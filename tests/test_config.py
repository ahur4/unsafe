"""Shared options, rendering, and the generic worker helper."""

import logging

import pytest

from unsafe.config import (
    Options,
    get_options,
    map_concurrent,
    render,
    set_options,
    use_options,
)


def test_defaults_and_immutability():
    options = Options(headers={"A": "1"})
    assert options.timeout == 10.0
    assert options.concurrency == 1
    assert options.verbosity == 0
    assert options.output_format == "text"
    assert options.max_attempts == 3
    assert options.backoff_factor == 0.5
    assert options.retry_statuses == (429, 500, 502, 503, 504)
    assert options.retry_methods == ("GET", "HEAD", "OPTIONS")
    with pytest.raises(TypeError):
        options.headers["A"] = "2"
    raw = {"A": "1"}
    frozen = Options(headers=raw)
    raw["A"] = "changed"
    assert frozen.headers["A"] == "1"


def test_replace_is_wholesale_for_headers():
    updated = Options(headers={"A": "1"}, timeout=4).replace(headers={"B": "2"})
    assert dict(updated.headers) == {"B": "2"}
    assert updated.timeout == 4


@pytest.mark.parametrize(
    "kwargs",
    [
        {"timeout": 0},
        {"timeout": -1},
        {"timeout": True},
        {"concurrency": 0},
        {"concurrency": False},
        {"verbosity": -1},
        {"max_attempts": 0},
        {"backoff_factor": -0.1},
        {"output_format": "xml"},
        {"retry_statuses": (99,)},
        {"retry_statuses": (True,)},
        {"retry_methods": ("",)},
        {"headers": {1: "a"}},
        {"headers": "nope"},
        {"proxies": "nope"},
        {"proxies": {"http": 1}},
    ],
)
def test_invalid_options_are_rejected(kwargs):
    with pytest.raises((TypeError, ValueError)):
        Options(**kwargs)


def test_use_options_restores_previous_values():
    set_options(Options(timeout=3, verbosity=1))
    assert logging.getLogger("unsafe").level == logging.INFO
    with pytest.raises(RuntimeError):
        with use_options(timeout=9, verbosity=2) as current:
            assert current.timeout == 9
            assert get_options().verbosity == 2
            assert logging.getLogger("unsafe").level == logging.DEBUG
            raise RuntimeError("boom")
    assert get_options().timeout == 3
    assert logging.getLogger("unsafe").level == logging.INFO
    with pytest.raises(TypeError):
        set_options("nope")


def test_render_text_and_json():
    payload = {"b": 1, "a": ["x"]}
    assert render(payload) == "b: 1\na: ['x']"
    assert render(["one", "two"]) == "one\ntwo"
    assert render("plain") == "plain"
    rendered = render(payload, Options(output_format="JSON"))
    assert rendered.index('"a"') < rendered.index('"b"')
    assert "\n" in rendered


def test_map_concurrent_preserves_order():
    sequential = map_concurrent(lambda value: value * 2, range(6), Options(concurrency=1))
    parallel = map_concurrent(lambda value: value * 2, range(6), Options(concurrency=4))
    assert sequential == parallel == [0, 2, 4, 6, 8, 10]
    assert map_concurrent(lambda value: value, [], Options(concurrency=4)) == []
