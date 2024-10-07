import concurrent.futures
from queue import Queue
from socket import gethostbyname, gaierror
from typing import Dict

from unsafe.strings.subdomains import subdomain


def protocol_cleaner(domain: str) -> str:
    """Cleans the protocol from the domain URL, ensuring no 'http://' or 'https://'."""
    return domain.replace("http://", "").replace("https://", "")


def resolve_subdomain(full_domain: str) -> str:
    """Attempts to resolve the subdomain to an IP address."""
    try:
        return gethostbyname(full_domain)
    except gaierror:
        return {}


def _send_req_cloudflare_bypasser_subdomain(domain: str, links_queue: Queue) -> Dict[str, str]:
    """
    Attempts to resolve subdomains to IP addresses using DNS lookup.

    :param domain: The root domain to which subdomains will be added.
    :param links_queue: A queue of subdomains to resolve.
    :return: A dictionary of subdomains and their resolved IP addresses.
    """
    cleaned_domain = protocol_cleaner(domain)
    results = {}

    while not links_queue.empty():
        subdomain = links_queue.get()
        full_domain = f'{subdomain}.{cleaned_domain}'

        ip_address = resolve_subdomain(full_domain)
        if ip_address:
            results[full_domain] = ip_address

        links_queue.task_done()

    return results


def cloud_bypasser(domain: str, subdomains: list = subdomain, worker: int = 5) -> Dict:
    data_queue: Queue = Queue()
    for sub in subdomains:
        data_queue.put(sub)
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = []
        for _ in range(worker):
            process = executor.submit(_send_req_cloudflare_bypasser_subdomain, domain, data_queue)
            futures.append(process)
        complete_result = {}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not None:
                complete_result.update(res)
        return complete_result


if __name__ == "__main__":
    print(cloud_bypasser("sabzlearn.ir"))
    # output :
    # {
    #     'www.sabzlearn.ir': '136.243.61.121', 'mail.sabzlearn.ir': '136.243.61.121',
    #     'chat.sabzlearn.ir': '80.249.115.108', 'status.sabzlearn.ir': '185.73.226.51',
    #     'tech.sabzlearn.ir': '80.249.115.193', 'webmail.sabzlearn.ir': '136.243.61.121',
    #     'files.sabzlearn.ir': '185.78.22.52', 'up.sabzlearn.ir': '80.249.115.194',
    #     'dl.sabzlearn.ir': '185.78.22.52', 'beta.sabzlearn.ir': '185.143.233.120',
    #     'erp.sabzlearn.ir': '185.18.215.17'
    # }
