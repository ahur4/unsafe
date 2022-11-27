import requests
import threading
import time
import json
from strings import wp_plugins1, wp_plugins2
from .. import NotWordpress, SiteNotFound, UsersFileNotFound, NotFoundData

plugins_list = []
counter = 0


class Wordpress:

    def __init__(self):
        pass

    async def wp_checker(self, domain: str):
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

    async def user(self, domain: str):
        try:
            if 'http://' in domain:
                domain = domain.replace('http://', '')
            elif 'https://' in domain:
                domain = domain.replace('https://', '')
            else:
                domain = domain
            if not await self.wp_checker(domain):
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
                User = 'Not Found!'
            return User
        except json.decoder.JSONDecodeError:
            raise NotWordpress(domain)
        except requests.exceptions.ConnectionError:
            raise SiteNotFound(domain)
        except KeyError:
            raise UsersFileNotFound
        except Exception as e:
            raise e

    def send_request(self, plugins: list, url: str):
        global plugins_list
        global counter
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
                print(counter)

    def main(self, url: str):
        if not self.wp_checker(url):
            return 'not wp'
        if 'http://' in url:
            url = url.replace('http://', '')
        elif 'https://' in url:
            url = url.replace('https://', '')
        else:
            url = url
        t1 = threading.Thread(target=self.send_request,
                              args=(wp_plugins1, url))
        t2 = threading.Thread(target=self.send_request,
                              args=(wp_plugins2, url))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        global plugins_list
        if plugins_list == []:
            raise NotFoundData

        else: return plugins_list