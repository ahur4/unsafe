import requests
import bs4
from urllib.parse import urlparse, parse_qs
from typing import Optional
from unsafe.utils.strings import ua
import json
import random
import string
import re


class Crawler:
    def __init__(self):
        ...

    def _string_generator(self, size=7, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

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

    def browser_search(self, query: str, timeout: int = 10, proxy: Optional[str] = None):
        res = []
        if proxy:
            google = requests.get(
                f'https://google.com/search?q={query}', timeout=timeout, proxies={"http": proxy, "https": proxy})
            bing = requests.get(
                f'https://www.bing.com/search?q={query}', timeout=timeout, proxies={"http": proxy, "https": proxy})
            ask = requests.get(
                f'https://www.ask.com/web?q={query}', timeout=timeout, proxies={"http": proxy, "https": proxy})
        else:
            google = requests.get(
                f'https://google.com/search?q={query}', timeout=timeout)
            bing = requests.get(
                f'https://www.bing.com/search?q={query}', timeout=timeout)
            ask = requests.get(
                f'https://www.ask.com/web?q={query}', timeout=timeout)

        soup = bs4.BeautifulSoup(google.text, "html.parser")
        try:
            anchors = soup.find(id='search').findAll('a')
        except AttributeError:
            gbar = soup.find(id='gbar')
            if gbar:
                gbar.clear()
            anchors = soup.findAll('a')
        for i in anchors:
            if self._filter_result(i["href"]):
                res.append(self._filter_result(i["href"]))
            else:
                pass
        ######################
        if "There are no results for" not in bing.text:
            soup = bs4.BeautifulSoup(bing.text,  "html.parser")
            try:
                anchors = soup.find(id='b_results').findAll("a")
                for i in anchors:
                    res.append(i["href"])
            except:
                ...
        ######################
        soup = bs4.BeautifulSoup(ask.text,  "html.parser")
        try:
            anchors = soup.find(
                attrs={"class": "PartialSearchResults-results"}).findAll("a")
            for i in anchors:
                res.append(i["href"])
        except:
            ...
        ######################
        return list(set(res))

    def link_extractor(self, source):
        before_result = []
        result = []
        for i in source.split('\n'):
            try:
                regexed = re.search(
                    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)", i)
                if regexed:
                    before_result.append(regexed)
            except:
                pass
        for i in before_result:
            result.append(i.group())
        return result

    def phone_extractor(self, source: str):
        before_result = []
        result = []
        for i in source.split('\n'):
            i = i.replace("۱", "1")
            i = i.replace("۲", "2")
            i = i.replace("۳", "3")
            i = i.replace("۴", "4")
            i = i.replace("۵", "5")
            i = i.replace("۶", "6")
            i = i.replace("۷", "7")
            i = i.replace("۸", "8")
            i = i.replace("۹", "9")
            i = i.replace("۰", "0")
            try:
                regexed = re.search(
                    r"(\+|00)[1-9][0-9 \-\(\)\.]{7,32}", i)
                if regexed:
                    before_result.append(regexed)
            except:
                pass
        for i in before_result:
            result.append(i.group())
        return result

    def username_extractor(self, source: str):
        before_result = []
        result = []
        for i in source.split('\n'):
            try:
                regexed = re.search(
                    r"(?<![\w@])@([\w@]+(?:[.!][\w@]+)*)", i)
                if regexed:
                    before_result.append(regexed)
            except:
                pass
        for i in before_result:
            result.append(i.group())
        return result

    def email_extractor(self, source: str):
        before_result = []
        result = []
        for i in source.split('\n'):
            try:
                regexed = re.search(
                    r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", i)
                if regexed:
                    before_result.append(regexed)
            except:
                pass
        for i in before_result:
            result.append(i.group())
        return result

    def crawl_single_page(self, url: str, timeout: int = 10, proxy: Optional[str] = None, proxies: Optional[list] = None):
        if "http://" in url:
            url = url.replace("http://", "")
        elif "https://" in url:
            url = url.replace("https://", "")
        else:
            ...
        url = "http://" + url
        
        if proxy:
            proxies = {"http": proxy, "https": proxy}
        elif proxies:
            p = random.choice(proxies)
            proxies = {"http": p, "https": p}
        else:
            r = requests.get(url, timeout=timeout)
            return {
                "links": self.link_extractor(r.text),
                "phones": self.phone_extractor(r.text),
                "usernames": self.username_extractor(r.text),
                "emails": self.email_extractor(r.text)
            }
        r = requests.get(url, timeout=timeout, proxies=proxies)
        return {
                "links": self.link_extractor(r.text),
                "phones": self.phone_extractor(r.text),
                "usernames": self.username_extractor(r.text),
                "emails": self.email_extractor(r.text)
            }

# a = Crawler()
# print(a.browser_search('"ahura" site:instagram.com'))
# # r = requests.get("https://www.iranair.de/fa/contact-us.html")
# print(a.crawl_single_page("https://www.iranair.de/fa/contact-us.html"))
# # print(a.link_extractor(r.text))
# # print(a.phone_extractor(r.text))
# # print(a.username_extractor(r.text))
# # #
