import requests
import threading
import time
import json
from unsafe.strings import wp_plugins
from unsafe.exceptions import NotWordpress, SiteNotFound, UsersFileNotFound, NotFoundData
from unsafe.proxies.proxy import Proxy

plugins_list = []
counter = 0


class Wordpress:

    def __init__(self):
        pass

    def wp_checker(self, domain: str):
        if 'http://' in domain:
            domain = domain.replace('http://', '')
        elif 'https://' in domain:
            domain = domain.replace('https://', '')
        else:
            domain = domain
        try:
            s = requests.get("http://"+domain+"/wp-content/plugins/")
            if s.history:
                return False
        except requests.exceptions.ConnectionError:
            return False
        if s.status_code == 404 or s.status_code == 500:
            return False
        return True

    def get_user(self, domain: str):
        try:
            if 'http://' in domain:
                domain = domain.replace('http://', '')
            elif 'https://' in domain:
                domain = domain.replace('https://', '')
            else:
                domain = domain
            if not self.wp_checker(domain):
                raise NotWordpress(domain)
        except:
            pass
        try:
            r = requests.get("https://"+domain+'/wp-json/wp/v2/users/').text
            j = json.loads(r)
            Count = len(j) - 1
            users_list = []
            cn = 0
            User = ''
            for Val in j:
                Split = '\n'
                if Count == cn:
                    Split = ''
                U = j[cn]['slug']
                if not U == '':
                    User += U+Split
                cn += 1
            if User == '':
                raise NotFoundData
            return User
        except json.decoder.JSONDecodeError:
            raise NotWordpress(domain)
        except requests.exceptions.ConnectionError:
            raise SiteNotFound(domain)
        except KeyError:
            raise UsersFileNotFound
        except Exception as e:
            raise e

    def send_request(self, plugins: list, url: str, timeout: int, auto_proxy: bool, proxy: list | str = None):
        global plugins_list
        global counter
        if auto_proxy:
            proxies = []
            ins_proxy = Proxy()
            proxies_dict = ins_proxy.wrapper('http', 100)
            for host, port in proxies_dict.items():
                checking = ins_proxy.checker(host, port, 'http', 10)
                if checking:
                    proxies.append(f'http://{host}:{port}')
                else:
                    pass
        for plus in plugins:
            counter += 1
            time.sleep(0.1)
            try:
                r = requests.get(f"http://{url}/wp-content/plugins/{plus}")
                if r.status_code == 200:
                    plugins_list.append(
                        f"http://{url}/wp-content/plugins/{plus}")
                else:
                    pass
            except Exception as e:
                raise e

    def plugin_scanner(self, url: str, timeout: int = 5, workers: int = 3, auto_proxy: bool = True, proxy: list | str = None):
        if not self.wp_checker(url):
            raise NotWordpress(url)
        if 'http://' in url:
            url = url.replace('http://', '')
        elif 'https://' in url:
            url = url.replace('https://', '')
        else:
            url = url
        if proxy:
            auto_proxy = False
        else:
            auto_proxy = True
        
        counter = 0
        for i in range(workers):
            counter += 1
            t = threading.Thread(target=self.send_request, args=())

        global plugins_list
        if plugins_list == []:
            raise NotFoundData

        else:
            return plugins_list
