from unsafe.utils.encrypt import Encryptor
from unsafe.utils.decrypt import Decrypter
from unsafe.utils.proxy import Proxy
from unsafe.utils.bruteforce import BruteForcer
from unsafe.utils.wp import Wordpress
from unsafe.utils.forensic import Forensic
from unsafe.utils.crawler import Crawler
from unsafe.utils.network import Network
from queue import Queue


class Unsafe(
    Encryptor,
    Decrypter,
    Proxy,
    BruteForcer,
    Wordpress,
    Forensic,
    Crawler,
    Network
):
    def __init__(self):
        self.admin_finder_queue = Queue()
        self.file_manager_queue = Queue()
        self.cloudflare_subdomain_bypasser = Queue()
        self.zip_cracker_queue = Queue()
        self.subdomain_scanner_queue = Queue()
        self.admin_finder_founded = []
        self.file_manager_founded = []
        self.subdomain_bypassed = {}
        self.zip_threads = []
        self.zip_password_founded = []
        self.subdomain_founded = []
