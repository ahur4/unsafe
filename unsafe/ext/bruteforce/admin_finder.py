import concurrent.futures
import random
from enum import Enum
from queue import Queue
from typing import Optional, List, Dict

import requests

from unsafe.strings.logins import (
    js_login, html_login, cfm_login, cgi_login, php_login,
    asp_login, aspx_login, brf_login, slash_login
)
from unsafe.strings.user_agents import ua


class Extensions(str, Enum):
    PHP = "php"
    JAVASCRIPT = "js"
    SLASH = "slash"
    ASP = "asp"
    ASPX = "aspx"
    HTML = "html"
    CGI = "cgi"
    CFM = "cfm"
    BRF = "brf"


def protocol_cleaner(domain: str) -> str:
    """Cleans the protocol from the domain URL, ensuring no 'http://' or 'https://'."""
    return domain.replace("http://", "").replace("https://", "")


def build_proxy(proxy: Optional[str], proxies: Optional[List[str]]) -> Optional[Dict[str, str]]:
    """Builds and returns the proxy dictionary for requests."""
    if proxy:
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    elif proxies:
        random_proxy = random.choice(proxies)
        return {"http": f"http://{random_proxy}", "https": f"http://{random_proxy}"}
    return None


def build_headers(user_agent: Optional[str], cookie: Optional[str], random_agent: bool) -> Dict[str, str]:
    """Builds and returns the headers for requests."""
    headers = {}
    if not user_agent and random_agent:
        headers["User-Agent"] = random.choice(ua)
    elif user_agent:
        headers["User-Agent"] = user_agent

    if cookie:
        headers["Cookie"] = cookie

    return headers


def _send_req_admin_finder(
        domain: str, timeout: int, links_queue, user_agent: Optional[str] = None,
        cookie: Optional[str] = None, proxy: Optional[str] = None,
        proxies: Optional[List[str]] = None, random_agent: bool = False
) -> List[str]:
    """Sends requests to find admin pages, using proxy, headers, and other configurations."""
    cleaned_domain = f"https://{protocol_cleaner(domain).rstrip('/')}"
    results = []
    proxy_dict = build_proxy(proxy, proxies)
    headers = build_headers(user_agent, cookie, random_agent)

    while not links_queue.empty():
        path = links_queue.get()
        full_link = f"{cleaned_domain}{path}"

        try:
            response = requests.get(
                url=full_link, headers=headers, allow_redirects=False,
                proxies=proxy_dict, timeout=timeout, verify=True,
            )
            if response.status_code == 200:
                results.append(full_link)
        except (requests.RequestException, KeyboardInterrupt):
            # In case of any network error or interruption, return the results so far
            return results if results else []

        links_queue.task_done()

    return results


def admin_finder(
        domain: str, timeout: int = 10, user_agent: Optional[str] = None, cookie: Optional[str] = None,
        extension: Extensions = Extensions.PHP, proxy: Optional[str] = None, proxies: Optional[List[str]] = None,
        random_agent: bool = False, worker: int = 5
) -> List[str]:
    if not isinstance(extension, Extensions):
        raise TypeError("Extensions can only be used with Extension data class")

    data_queue: Queue = Queue()
    if extension == Extensions.PHP:
        for login in php_login:
            data_queue.put(login)
    elif extension == Extensions.JAVASCRIPT:
        for login in js_login:
            data_queue.put(login)
    elif extension == Extensions.SLASH:
        for login in slash_login:
            data_queue.put(login)
    elif extension == Extensions.ASP:
        for login in asp_login:
            data_queue.put(login)
    elif extension == Extensions.ASPX:
        for login in aspx_login:
            data_queue.put(login)
    elif extension == Extensions.HTML:
        for login in html_login:
            data_queue.put(login)
    elif extension == Extensions.CGI:
        for login in cgi_login:
            data_queue.put(login)
    elif extension == Extensions.CFM:
        for login in cfm_login:
            data_queue.put(login)
    elif extension == Extensions.BRF:
        for login in brf_login:
            data_queue.put(login)
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = []
        for _ in range(worker):
            process = executor.submit(
                _send_req_admin_finder,
                domain=domain, timeout=timeout, links_queue=data_queue, user_agent=user_agent, cookie=cookie,
                proxy=proxy, proxies=proxies, random_agent=random_agent
            )
            futures.append(process)
        complete_result = []
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not None:
                complete_result += res
        return complete_result


if __name__ == "__main__":
    print(admin_finder("portal.saorg.ir", random_agent=True))  # ['https://portal.saorg.ir/wp-login.php']
