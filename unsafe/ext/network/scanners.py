import socket
from typing import Optional, List


def _port_scanner(host: str, port: int) -> bool:
    """Checks if a specific port on the host is open.

    Args:
        host (str): The target host.
        port (int): The port to check.

    Returns:
        bool: True if the port is open, False otherwise.
    """
    with socket.socket() as s:
        try:
            s.settimeout(0.2)
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False


def port_scanner(host: str, ports: Optional[List[int]] = None, port: Optional[int] = None) -> List[int]:
    """Scans the specified port(s) on the target host to check if they are open.

    Args:
        host (str): The target host.
        ports (Optional[List[int]]): A list of ports to scan. Defaults to None.
        port (Optional[int]): A single port to scan. Defaults to None.

    Returns:
        List[int]: A list of open ports.
    """
    open_ports = []

    # Scan multiple ports if provided
    if ports:
        for p in ports:
            if _port_scanner(host, p):
                open_ports.append(p)

    # Scan a single port if provided
    elif port:
        if _port_scanner(host, port):
            open_ports.append(port)

    return open_ports
