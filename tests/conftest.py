"""Keep option changes from leaking between tests."""

import pytest

from unsafe.config import Options, set_options


@pytest.fixture(autouse=True)
def _reset_options():
    set_options(Options())
    yield
    set_options(Options())
