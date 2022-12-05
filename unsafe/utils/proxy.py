from bs4 import BeautifulSoup
import requests
import socks

TIMEOUT = (3.05, 27)
URL = "http://google.com"


class Proxy:
    """Proxy"""

    def __init__(self) -> None:
        pass

    def wrapper(self, protocol: str = "http", max_ping: int = 200) -> dict:
        """
        ### This Method Crawl a Site For Get Proxie's

        it Takes The Following Arguments:

        * protocol : Proxy Protocol. (Default=http)
        * max_ping : Maximum Ping of Proxy. (Default=200)
        * Available Protocol's : http, socks4, socks5

        * #### return: dictionary
        
        ```
        proxy = Proxy()
        proxylist = proxy.wrapper(protocol = "socks4", max_ping = 100)
        ```
        """
        if protocol.lower() in ["http", "socks5", "socks4"]:
            #Send Request
            req = requests.get(
                f'https://www.freeproxy.world/?type={protocol}&anonymity=&country=&speed={max_ping}&port=&page=1')

            #Create Object and Select Parser Type
            soup = BeautifulSoup(req.text, 'html.parser')

            #Find All Proxy IP's and Port's
            ips = soup.find_all('td', class_='show-ip-div')
            ports = soup.find_all('a')

            list_ip = [str(ip.contents[0].replace('\n', '')) for ip in ips]

            list_port = []

            for i in ports:
                i = i.get_text()
                try:
                    int(i)
                    list_port.append(i)
                except:
                    pass

            #Ordering Proxies
            proxy_list = dict(zip(list_ip, list_port))

            return proxy_list
        else:
            raise ValueError("This Protocol Not Exists.")

    def checker(self, proxy_host: str, proxy_port: str, protocol: str = "http", timeout: int = 2) -> bool:
        """
        ### This Function is to Check if The Proxy is Dead or Not.

        it Takes The Following Arguments:

        * proxy_host: Proxy's IP
        * proxy_port: Proxy's PORT
        * protocol: http, socks4 or socks5 (Default = http)
        * timeout: The Connection's Timeout (Default = 5)
        
        * #### return: boolean
        
        ```
        proxy = Proxy()
        proxy_check = proxy.wrapper(proxy_host = "10.255.36.45", proxy_port = "80", protocol = "socks4", timeout = 2)
        ```
        """
        proxy_status = False
        if (protocol == "http") or (protocol == "https"):
            try:
                requests.get(
                    "http://www.google.com",
                    proxies={protocol: "http://" +
                             str(proxy_host) + ":" + str(proxy_port)},
                    timeout=timeout,
                )
                proxy_status = True
            except:
                pass
        elif protocol == "socks4":
            try:
                socks4_test = socks.socksocket()
                socks4_test.setproxy(
                    socks.PROXY_TYPE_SOCKS4, proxy_host, proxy_port, True)
                socks4_test.settimeout(timeout)
                socks4_test.connect(("www.google.com", 80))
                proxy_status = True
            except:
                pass
        elif protocol == "socks5":
            try:
                socks5_test = socks.socksocket()
                socks5_test.setproxy(
                    socks.PROXY_TYPE_SOCKS5, proxy_host, proxy_port, True)
                socks5_test.settimeout(timeout)
                socks5_test.connect(("www.google.com", 80))
                proxy_status = True
            except:
                pass
        return proxy_status
