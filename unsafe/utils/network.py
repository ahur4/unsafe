import socket
from threading import Thread
from typing import Optional
from unsafe.utils.strings import mac_addresses_list

class Network:
    def __init__(self):
        ...

    def _port_scanner(self, host: str, port: int):
        _socket = socket.socket()
        try:
            _socket.settimeout(0.2)
            _socket.connect((host, port))
        except:
            return False
        return True

    def port_scanner(self, host: str, ports: Optional[list] = None, port: Optional[int] = None):
        open_ports = []
        if ports:
            for i in ports:
                if self._port_scanner(host=host, port=int(i)):
                    open_ports.append(int(i))
                else:
                    ...
        elif port:
            if self._port_scanner(host=host, port=int(port)):
                open_ports.append(int(port))
            else:
                ...
        return open_ports

    def mac_address_lookup(self, mac: str):
        mac = mac.upper().replace(':', '')
        if len(mac) == 6:
            try:
                return mac_addresses_list[mac.strip()]
            except:
                return ''
        elif len(mac) < 6:
            raise KeyError('Invalid mac address')
        else:
            try:
                return mac_addresses_list[mac[:6].strip()]
            except:
                return ''

