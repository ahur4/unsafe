import random
import re
import string
from typing import Optional, List
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup as bs


def string_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def filter_result(link: str) -> Optional[str]:
    """Filter out non-relevant URLs."""
    try:
        if link.startswith('/url?'):
            o = urlparse(link, 'http')
            link = parse_qs(o.query)['q'][0]
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link
    except Exception:
        return None


def extract_links_from_html(html: str) -> List[str]:
    """Extract valid URLs from HTML content."""
    regex = re.compile(
        r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)"
    )
    return list(set(data[1] for data in re.findall(regex, html)))


def extract_phones_from_text(text: str) -> List[str]:
    """Extract phone numbers from the given text."""
    text = text.translate(str.maketrans('۱۲۳۴۵۶۷۸۹۰', '1234567890'))  # Replace Persian digits
    regex = re.compile(r"(\+98|0)?9\d{9}|(\+|00)[1-9][0-9 \-()\.]{7,32}$|0[1-8]{2}[0-9]{8}")
    return list(set([match.group() for match in re.finditer(regex, text)]))


def extract_emails_from_text(text: str) -> List[str]:
    """Extract email addresses from the given text."""
    regex = re.compile(
        r'(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3'
        r'}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))'
    )
    return list(set([match.group() for match in re.finditer(regex, text)]))


def extract_usernames_from_text(text: str) -> List[str]:
    """Extract usernames from the given text."""
    regex = re.compile(r"(?<![\w@])@([\w@]+(?:[.!][\w@]+)*)")
    return list(set([match.group() for match in re.finditer(regex, text)]))


def search_browser(query: str, timeout: int = 10, proxy: Optional[str] = None) -> List[str]:
    """Searches Google, Bing, and Ask for the given query."""
    search_engines = [
        f'https://google.com/search?q={query}',
        f'https://www.bing.com/search?q={query}',
        f'https://www.ask.com/web?q={query}'
    ]
    results = []
    for engine in search_engines:
        try:
            response = requests.get(engine, timeout=timeout, proxies={"http": proxy, "https": proxy} if proxy else None)
            soup = bs(response.text, "html.parser")
            anchors = soup.find_all('a')
            for anchor in anchors:
                filtered = filter_result(anchor.get("href", ""))
                if filtered:
                    results.append(filtered)
        except Exception:
            continue
    return list(set(results))


def crawl_page(url: str, timeout: int = 10, proxy: Optional[str] = None) -> dict:
    """Crawls a page and extracts emails, phones, links, and usernames."""
    try:
        response = requests.get(url, timeout=timeout, proxies={"http": proxy, "https": proxy} if proxy else None)
        html = response.text
        return {
            "links": extract_links_from_html(html),
            "phones": extract_phones_from_text(html),
            "emails": extract_emails_from_text(html),
            "usernames": extract_usernames_from_text(html)
        }
    except Exception:
        return {"links": [], "phones": [], "emails": [], "usernames": []}



if __name__ == "__main__":
    print(crawl_page("https://irancell.ir/p/1590/contact-us"))
