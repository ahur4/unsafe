import concurrent.futures
from queue import Queue
from typing import Optional

import requests

from unsafe.strings.wordpress import wp_plugins


def protocol_cleaner(domain: str) -> str:
    """Cleans the protocol from the domain URL, ensuring no 'http://' or 'https://'."""
    return domain.replace("http://", "").replace("https://", "")


def _send_request(
        domain: str, plugins_queue: Queue, timeout: int = 10,
        proxy: Optional[str] = None
):
    results = []
    proxies = {"https": f"{proxy}", "http": f"{proxy}"} if proxy else {}
    while not plugins_queue.empty():
        data = plugins_queue.get()
        req = requests.get(
            url=f"https://{domain}/wp-content/plugins/{data}",
            timeout=timeout, proxies=proxies
        )
        if req.status_code == 200:
            results.append(data)
        plugins_queue.task_done()
    return results


def plugin_scanner(
        domain: str, timeout: int = 10, proxy: Optional[str] = None, worker: int = 5
):
    data_queue: Queue = Queue()
    for plugin in wp_plugins:
        data_queue.put(plugin)
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = []
        for _ in range(worker):
            process = executor.submit(
                _send_request,
                domain, data_queue, timeout, proxy
            )
            futures.append(process)
        complete_result = []
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not None:
                complete_result += res
        return complete_result
