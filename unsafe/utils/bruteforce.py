from unsafe.utils.strings import aspx_login, asp_login, php_login, html_login, cgi_login, brf_login, cfm_login, js_login, slash_login, ua, manager, subdomain
import requests
import random
from threading import Thread
from queue import Queue
from socket import gethostbyname
from typing import Optional

class BruteForcer:

    def __init__(self) -> None:
        self.admin_finder_queue = Queue()
        self.file_manager_queue = Queue()
        self.cloudflare_subdomain_bypasser = Queue()
        self.admin_finder_founded = []
        self.file_manager_founded = []
        self.subdomain_bypassed = {}

    def _send_req_admin_finder(self, domain: str, timeout: int, links_queue, user_agent: Optional[str] = None,
                               cookie: Optional[str] = None, proxy: Optional[str] = None, proxies: Optional[list] = None):

        if "http://" in domain:
            domain = domain.replace("http://", "")
        elif "https://" in domain:
            domain = domain.replace("https://", "")
        else:
            ...
        domain = "http://" + domain
        while not links_queue.empty():
            i = links_queue.get()
            try:
                if proxy:
                    proxy = {"http": "http://" +
                             str(proxy), "https": "http://" + str(proxy)}
                elif proxies:
                    random_proxy = random.choice(proxies)
                    proxy = {
                        "http": "http://" + str(random_proxy), "https": "http://" + str(random_proxy)}
                if not user_agent:
                    user_agent = random.choice(ua)
                header = {"User-Agent": user_agent}
                if cookie:
                    header.update({"Cookie": cookie})
                if domain[len(domain) - 1] == "/":
                    domain = domain[0: len(domain) - 1]

                full_link = domain + i
                try:
                    if proxy or proxies:
                        r = requests.get(
                            full_link,
                            headers=header,
                            allow_redirects=False,
                            proxies=proxy,
                            timeout=timeout,
                            verify=False,
                        )
                    else:
                        r = requests.get(
                            full_link,
                            headers=header,
                            allow_redirects=False,
                            timeout=timeout,
                            verify=False,
                        )
                except Exception as e:
                    if len(self.admin_finder_founded) >= 1:
                        return self.admin_finder_founded
                    else:
                        return []
                links_queue.task_done()
                if r.status_code == 200:
                    self.admin_finder_founded.append(full_link)
                else:
                    ...
            except KeyboardInterrupt:
                break

        return self.admin_finder_founded

    def admin_finder(self, domain: str, workers: int = 3, timeout: int = 10, ext: str = "php", user_agent: Optional[str] = None,
                     cookie: Optional[str] = None, proxy: Optional[str] = None, proxies: Optional[list] = None):
        threads = []
        links = []
        self.admin_finder_founded.clear()
        ext = ext.strip().lower()
        if ext == "php":
            links = php_login
        elif ext == "asp":
            links = asp_login
        elif ext == "aspx":
            links = aspx_login
        elif ext == "js":
            links = js_login
        elif ext == "slash":
            links = slash_login
        elif ext == "cfm":
            links = cfm_login
        elif ext == "cgi":
            links = cgi_login
        elif ext == "brf":
            links = brf_login
        elif ext == "html":
            links = html_login
        else:
            raise ValueError("This ext(Argument) Not Allowed !")
        for i in links:
            self.admin_finder_queue.put(i)
        for i in range(workers):
            thread_ = Thread(target=self._send_req_admin_finder, args=(
                domain, timeout, self.admin_finder_queue, user_agent, cookie, proxy, proxies))
            thread_.setDaemon(True)
            thread_.start()
            threads.append(thread_)
        for i in threads:
            i.join()
        return self.admin_finder_founded

    def _send_req_file_manager(self, domain: str, timeout: int, links_queue, user_agent: Optional[str] = None,
                               cookie: Optional[str] = None, proxy: Optional[str] = None, proxies: Optional[list] = None):

        if "http://" in domain:
            domain = domain.replace("http://", "")
        elif "https://" in domain:
            domain = domain.replace("https://", "")
        else:
            ...

        domain = "http://" + domain
        while not links_queue.empty():
            i = links_queue.get()
            try:
                if proxy:
                    proxy = {"http": "http://" +
                             str(proxy), "https": "http://" + str(proxy)}
                elif proxies:
                    random_proxy = random.choice(proxies)
                    proxy = {
                        "http": "http://" + str(random_proxy), "https": "http://" + str(random_proxy)}
                if not user_agent:
                    user_agent = random.choice(ua)
                header = {"User-Agent": user_agent}
                if cookie:
                    header.update({"Cookie": cookie})
                if domain[len(domain) - 1] == "/":
                    domain = domain[0: len(domain) - 1]

                full_link = domain + i
                try:
                    if proxy or proxies:
                        r = requests.get(
                            full_link,
                            headers=header,
                            allow_redirects=True,
                            proxies=proxy,
                            timeout=timeout,
                            verify=True,
                        )
                    else:
                        r = requests.get(
                            full_link,
                            headers=header,
                            allow_redirects=True,
                            timeout=timeout,
                            verify=True,
                        )
                except Exception as e:
                    if len(self.file_manager_founded) >= 1:
                        return self.file_manager_founded
                    else:
                        return []
                links_queue.task_done()
                if r.status_code == 200:
                    self.file_manager_founded.append(f"{r.url}")
                else:
                    ...
            except KeyboardInterrupt:
                break

        return self.file_manager_founded

    def filemanager_finder(self, domain: str, workers: int = 5, timeout: int = 5, user_agent: Optional[str] = None,
                           cookie: Optional[str] = None, proxy: Optional[str] = None, proxies: Optional[list] = None):
        threads = []
        self.file_manager_founded.clear()
        for i in manager:
            self.file_manager_queue.put(i)
        for i in range(workers):
            thread_ = Thread(target=self._send_req_file_manager, args=(
                domain, timeout, self.file_manager_queue, user_agent, cookie, proxy, proxies))
            thread_.setDaemon(True)
            thread_.start()
            threads.append(thread_)
        for i in threads:
            i.join()

        return self.file_manager_founded

    def _send_req_cloudflare_bypasser_subdomain(self, domain: str, links_queue):

        if "http://" in domain:
            domain = domain.replace("http://", "")
        elif "https://" in domain:
            domain = domain.replace("https://", "")
        else:
            ...

        # domain = "http://" + domain
        while not links_queue.empty():
            sub_domain = links_queue.get()
            full_link = f'{sub_domain}.{domain}'
            try:
                ip = gethostbyname(full_link)
                self.subdomain_bypassed.update({full_link: ip})
            except Exception as e:
                if len(self.subdomain_bypassed) >= 1:
                    return self.subdomain_bypassed
                else:
                    return {}
            links_queue.task_done()
        return self.subdomain_bypassed

    def cloudflare_bypasser(self, domain: str, workers: int = 5):
        threads = []
        self.subdomain_bypassed.clear()
        for i in subdomain:
            self.cloudflare_subdomain_bypasser.put(i)
        for i in range(workers):
            thread_ = Thread(target=self._send_req_cloudflare_bypasser_subdomain, args=(
                domain, self.cloudflare_subdomain_bypasser))
            thread_.setDaemon(True)
            thread_.start()
            threads.append(thread_)
        for i in threads:
            i.join()
        return self.subdomain_bypassed
