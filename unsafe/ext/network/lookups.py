"""Local MAC vendor lookup."""

from __future__ import annotations

from typing import Optional

from unsafe.models import MacVendor
from unsafe.strings.mac_addresses import mac_addresses_list


def mac_address_lookup(mac: str) -> MacVendor:
    """Look up the vendor for a MAC address prefix in the local table.

    Separators ``:`` and ``-`` are ignored. The result is a :class:`MacVendor`.
    ``vendor`` is ``None`` when the prefix is not in the table.

    Raises:
        KeyError: If the address has fewer than six hex digits.
    """
    if not isinstance(mac, str):
        raise TypeError("mac must be a string")
    compact = mac.upper().replace(":", "").replace("-", "").strip()
    if len(compact) < 6:
        raise KeyError("Invalid MAC address: Too short.")
    prefix = compact[:6]
    found = mac_addresses_list.get(prefix, "")
    vendor: Optional[str]
    if isinstance(found, str) and found:
        vendor = found
    else:
        vendor = None
    return MacVendor(address=mac, prefix=prefix, vendor=vendor)
