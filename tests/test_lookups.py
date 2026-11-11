"""Local MAC vendor lookup."""

import pytest

from unsafe.ext.network.lookups import mac_address_lookup


def test_known_prefix_ignores_separators_and_case():
    first = mac_address_lookup("00:00:5e:00:53:af")
    second = mac_address_lookup("00-00-5E-00-00-01")
    assert first.vendor == "U.S. Department of Defense (IANA)"
    assert second.vendor == first.vendor
    assert first.prefix == "00005E"
    assert first.model_dump()["vendor"] == first.vendor


def test_unknown_prefix_is_none():
    result = mac_address_lookup("02:00:00:00:00:00")
    assert result.vendor is None
    assert result.prefix == "020000"


def test_short_value_raises():
    with pytest.raises(KeyError):
        mac_address_lookup("00:11")
