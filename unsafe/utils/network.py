import socket
from threading import Thread
from typing import Optional


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


# a = Network()

# print(a.port_scanner('185.188.104.10', ports=[53, 80, 179, 225, 443]))
