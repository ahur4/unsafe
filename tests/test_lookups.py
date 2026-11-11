"""Local MAC vendor lookup."""

import pytest

from unsafe.ext.network.lookups import mac_address_lookup


def test_known_prefix_ignores_separators_and_case():
    assert mac_address_lookup("00:00:5e:00:53:af") == "U.S. Department of Defense (IANA)"
    assert mac_address_lookup("00-00-5E-00-00-01") == "U.S. Department of Defense (IANA)"


def test_unknown_prefix_is_empty_string():
    assert mac_address_lookup("02:00:00:00:00:00") == ""


def test_short_value_raises():
    with pytest.raises(KeyError):
        mac_address_lookup("00:11")
