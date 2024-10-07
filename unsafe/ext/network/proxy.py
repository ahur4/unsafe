import contextlib
from enum import Enum
from typing import List

import requests

SOCKS5_SOURCE_1 = 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt'
SOCKS4_SOURCE_1 = 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt'
HTTP_SOURCE_1 = 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt'


class ProxyType(str, Enum):
    HTTP = "http"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"


def proxy_tester(proxy: str, proxy_type: ProxyType, domain: str = 'www.google.com', timeout: int = 5) -> bool:
    if not isinstance(proxy_type, ProxyType):
        raise ValueError('Proxy must be of type ProxyType')
    proxies = {
        "http": f"{proxy_type.value}://{proxy}",
        "https": f"{proxy_type.value}://{proxy}",
    }
    with contextlib.suppress(requests.RequestException):
        response = requests.get(f"http://{domain}", proxies=proxies, timeout=timeout)
        if 200 <= response.status_code < 300:
            return True
    return False


def get_socks5_proxy() -> List[str]:
    socks5_proxy = []
    with contextlib.suppress(requests.RequestException):
        with requests.get(SOCKS5_SOURCE_1, timeout=5) as req:
            for line in req.text.splitlines():
                socks5_proxy.append(line)
    return socks5_proxy


def get_socks4_proxy() -> List[str]:
    socks4_proxy = []
    with contextlib.suppress(requests.RequestException):
        with requests.get(SOCKS4_SOURCE_1, timeout=5) as req:
            for line in req.text.splitlines():
                socks4_proxy.append(line)
    return socks4_proxy


def get_http_proxy() -> List[str]:
    http_proxy = []
    with contextlib.suppress(requests.RequestException):
        with requests.get(HTTP_SOURCE_1, timeout=5) as req:
            for line in req.text.splitlines():
                http_proxy.append(line)
    return http_proxy


