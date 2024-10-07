from unsafe.strings.mac_addresses import mac_addresses_list
from typing import Optional


def mac_address_lookup(mac: str) -> Optional[str]:
    """Looks up the vendor associated with a given MAC address prefix.

    Args:
        mac (str): The MAC address to lookup.

    Returns:
        Optional[str]: The vendor name if found, otherwise None.

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


if __name__ == '__main__':
    print(mac_address_lookup(mac="00-05-9A-3C-7A-00"))
