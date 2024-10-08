from unsafe import network

http_proxies = network.get_http_proxy()
chunk_proxies = http_proxies[:20]

valid_proxies = []

for proxy in chunk_proxies:
    tester = network.proxy_tester(
        proxy=proxy,
        proxy_type=network.ProxyType.HTTP,
        timeout=2
    )
    if tester:
        valid_proxies.append(proxy)

print("All Valid Proxies:", valid_proxies)
