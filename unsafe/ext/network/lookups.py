from unsafe.strings.mac_addresses import mac_addresses_list


def mac_address_lookup(mac: str) -> str:
    """Look up the vendor for a MAC address prefix in the local table.

    Args:
        mac: MAC address. Separators ``:`` and ``-`` are ignored.

    Returns:
        The vendor name. Unknown prefixes return an empty string.

    Raises:
        KeyError: If the MAC address is invalid (too short).
    """
    mac_prefix = mac.upper().replace(':', '').replace('-', '').strip()

    # Ensure the MAC address has enough length
    if len(mac_prefix) < 6:
        raise KeyError('Invalid MAC address: Too short.')

    # Use only the first 6 characters for lookup
    mac_prefix = mac_prefix[:6]

    # Return the vendor name if found, otherwise empty string
    return mac_addresses_list.get(mac_prefix, "")
