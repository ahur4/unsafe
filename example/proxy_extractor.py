from unsafe import Unsafe

unsafe = Unsafe()


def get_health_proxy(protocol: str = "http", max_ping: int = 200):
    healthy_proxy = {}

    #Extract a Number of Proxy
    proxies_dict = unsafe.proxy_wrapper(protocol=protocol, max_ping=max_ping)

    #Check Them with proxy_checker() Function
    for j, k in proxies_dict.items():
        isHealth = unsafe.proxy_checker(
            proxy_host=j,
            proxy_port=k,
            protocol=protocol,
            timeout=10
        )
        if isHealth:
            healthy_proxy[j] = k
        else:
            ...

    return healthy_proxy
