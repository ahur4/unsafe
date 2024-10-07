import concurrent.futures
import random
from queue import Queue
from typing import Optional, List, Dict

import requests

from unsafe.strings.file_managers import manager
from unsafe.strings.user_agents import ua


def protocol_cleaner(domain: str) -> str:
    """Cleans the protocol from the domain URL by removing 'http://' or 'https://'."""
    return domain.replace("http://", "").replace("https://", "")


def build_proxy(proxy: Optional[str], proxies: Optional[List[str]]) -> Optional[Dict[str, str]]:
    """Builds a proxy dictionary from either a single proxy or a list of proxies."""
    if proxy:
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    elif proxies:
        random_proxy = random.choice(proxies)
        return {"http": f"http://{random_proxy}", "https": f"http://{random_proxy}"}
    return None


def build_headers(user_agent: Optional[str], cookie: Optional[str], random_agent: bool) -> Dict[str, str]:
    """Builds the headers for the request, including User-Agent and cookies if provided."""
    headers = {}
    if not user_agent and random_agent:
        headers["User-Agent"] = random.choice(ua)
    elif user_agent:
        headers["User-Agent"] = user_agent

    if cookie:
        headers["Cookie"] = cookie

    return headers


def _send_req_file_manager(
        domain: str, timeout: int, links_queue, user_agent: Optional[str] = None,
        cookie: Optional[str] = None, proxy: Optional[str] = None,
        proxies: Optional[List[str]] = None, random_agent: bool = False
) -> List[str]:
    """Sends requests to find file manager pages, using optional proxy, user-agent, and cookies."""
    cleaned_domain = f"https://{protocol_cleaner(domain).rstrip('/')}"
    results = []
    proxy_dict = build_proxy(proxy, proxies)
    headers = build_headers(user_agent, cookie, random_agent)

    while not links_queue.empty():
        endpoint = links_queue.get()
        full_url = f"{cleaned_domain}{endpoint}"

        try:
            response = requests.get(
                full_url, headers=headers, allow_redirects=True,
                proxies=proxy_dict, timeout=timeout, verify=True,
            )

            if response.status_code == 200:
                results.append(response.url)
        except requests.RequestException:
            # If there's a network error or exception, return current results
            return results if results else []

        links_queue.task_done()

    return results


def file_manager_finder(
        domain: str,
        timeout: int = 10, user_agent: Optional[str] = None, cookie: Optional[str] = None,
        proxy: Optional[str] = None, proxies: Optional[List[str]] = None, random_agent: bool = False,
        worker: int = 5
) -> List[str]:
    data_queue: Queue = Queue()
    for path in manager:
        data_queue.put(path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = []
        for _ in range(worker):
            process = executor.submit(
                _send_req_file_manager,
                domain, timeout, data_queue, user_agent,
                cookie, proxy, proxies, random_agent
            )
            futures.append(process)
        complete_result = []
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not None:
                complete_result += res
        return complete_result


if __name__ == "__main__":
    print(file_manager_finder("lacasadepinturas.com"))
    # output :
    # [
    #     'https://lacasadepinturas.com/js/filemanager/index.html',
    #     'https://lacasadepinturas.com/js/Filemanager/index.html'
    # ]
