from unsafe.utils.strings import aspx_login, asp_login, php_login, html_login, cgi_login, brf_login, cfm_login, js_login, slash_login, ua, manager
import requests
import random
from threading import Thread
from queue import Queue

admin_finder_queue = Queue()
file_manager_queue = Queue()
admin_finder_founded = []
file_manager_founded = []


class BruteForcer:

    def __init__(self) -> None:
        pass

    def send_req_admin_finder(self, domain: str, timeout: int, links_queue, user_agent: str | None = None,
                              cookie: str | None = None, proxy: str | None = None, proxies: list | None = None):

        if "http://" in domain:
            domain = domain.replace("http://", "")
        elif "https://" in domain:
            domain = domain.replace("https://", "")
        else:
            pass
        domain = "http://" + domain
        global admin_finder_founded
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
                    if len(admin_finder_founded) >= 1:
                        return admin_finder_founded
                    else:
                        return []
                links_queue.task_done()
                if r.status_code == 200:
                    admin_finder_founded.append(full_link)
                else:
                    pass
            except KeyboardInterrupt:
                break

        return admin_finder_founded

    def admin_finder(self, domain: str, workers: int = 3, timeout: int = 10, ext: str = "php", user_agent: str | None = None,
                     cookie: str | None = None, proxy: str | None = None, proxies: list | None = None):
        global admin_finder_queue
        global admin_finder_founded
        threads = []
        links = []
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
            admin_finder_queue.put(i)
        for i in range(workers):
            thread_ = Thread(target=self.send_req_admin_finder, args=(
                domain, timeout, admin_finder_queue, user_agent, cookie, proxy, proxies))
            thread_.setDaemon(True)
            thread_.start()
            threads.append(thread_)
        for i in threads:
            i.join()
        return admin_finder_founded

    def send_req_file_manager(self, domain: str, timeout: int, links_queue, user_agent: str | None = None,
                              cookie: str | None = None, proxy: str | None = None, proxies: list | None = None):

        if "http://" in domain:
            domain = domain.replace("http://", "")
        elif "https://" in domain:
            domain = domain.replace("https://", "")
        else:
            pass

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
                    if len(file_manager_founded) >= 1:
                        return file_manager_founded
                    else:
                        return []
                links_queue.task_done()
                print(r.status_code)
                if r.status_code == 200:
                    print(r.url)
                    file_manager_founded.append(f"{r.url}")
                    print(file_manager_founded)
                else:
                    pass
            except KeyboardInterrupt:
                break

        return file_manager_founded

    def filemanager_finder(self, domain: str, workers: int = 5, timeout: int = 5, user_agent: str | None = None,
                           cookie: str | None = None, proxy: str | None = None, proxies: list | None = None):
        global file_manager_queue
        threads = []
        for i in manager:
            file_manager_queue.put(i)
        for i in range(workers):
            thread_ = Thread(target=self.send_req_file_manager, args=(
                domain, timeout, file_manager_queue, user_agent, cookie, proxy, proxies))
            thread_.setDaemon(True)
            thread_.start()
            threads.append(thread_)
        for i in threads:
            i.join()
        response = file_manager_founded
        file_manager_founded.clear()
        return response
