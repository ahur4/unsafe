import requests
import bs4
from urllib.parse import urlparse, parse_qs
from typing import Optional
from unsafe.utils.strings import ua
import json, random

class Seeker:
    def __init__(self):
        ...

    def _filter_result(self, link: str):
        try:
            if link.startswith('/url?'):
                o = urlparse(link, 'http')
                link = parse_qs(o.query)['q'][0]
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link
        except Exception:
            ...

    def google_dorking(self, query: str, timeout: int = 10, proxy: Optional[str] = None):
        res = []
        if proxy:
            r = requests.get(
                f'https://google.com/search?q={query}', timeout=timeout, proxies={"http": proxy, "https": proxy})
        else:
            r = requests.get(
                f'https://google.com/search?q={query}', timeout=timeout)

        soup = bs4.BeautifulSoup(r.text, "html.parser")
        try:
            anchors = soup.find(id='search').findAll('a')
            # Sometimes (depending on the User-agent) there is
            # no id "search" in html response...
        except AttributeError:
            # Remove links of the top bar.
            gbar = soup.find(id='gbar')
            if gbar:
                gbar.clear()
            anchors = soup.findAll('a')
        for i in anchors:
            if self._filter_result(i["href"]):
                res.append(self._filter_result(i["href"]))
            else:
                pass
        return res



