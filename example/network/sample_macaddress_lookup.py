from unsafe import network

mac_address = "00:11:22:33:44:55:66"

lookup = network.mac_address_lookup(mac=mac_address)
if lookup is not None:
    print(lookup)
