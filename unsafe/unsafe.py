from unsafe.utils.encrypt import Encryptor
from unsafe.utils.decrypt import Decrypter
from unsafe.utils.proxy import Proxy
from unsafe.utils.bruteforce import BruteForcer
from unsafe.utils.wp import Wordpress
from unsafe.utils.exifdata import ExifImage
from unsafe.utils.anonymous import Anonymous
from unsafe.utils.seeker import Seeker
from queue import Queue


class Unsafe(
    Encryptor,
    Decrypter,
    Proxy,
    BruteForcer,
    Wordpress,
    ExifImage,
    Anonymous,
    Seeker
):
    def __init__(self):
        self.admin_finder_queue = Queue()
        self.file_manager_queue = Queue()
        self.cloudflare_subdomain_bypasser = Queue()
        self.admin_finder_founded = []
        self.file_manager_founded = []
        self.subdomain_bypassed = {}
