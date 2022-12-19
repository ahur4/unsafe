# unsafe

> A practical and optimal library for those interested in Pentest, cryptography,Vulnerability Scanner and ..!
> 
> Developed by Ahur4, MesutFD (™) 2022

## Examples of How To Use.

> - Hashing, Encrypting and Hash Cracking or Text Decryption
>> Available Mathods :
>> - MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SHA3-224, SHA3-256, SHA3-384, SHA3-512, SHAKE128, SHAKE256
>> - BASE16, BASE32, BASE64, BASE64, BASE85, ASCII85, CAESAR
>
>> p.s : for shake methods(128, 256) and caesar method you must use count parameter in calling function.
>>
>> p.s : in encryption and decryption all arguments are optional except words(in encrypt) and hash(in decrypt).
>>
>> p.s : for default wordlist there is John The Ripper's tool wordlist.

```python
>>> from unsafe import Encryptor, Decrypter
>>> dec = Decrypter()
>>> enc = Encryptor()
>>> my_md5 = enc.text_encrypt(words='unsafe', encode='UTF-8', hash_method='MD5')
>>> my_md5
'64c823fad1d87e0df1ef3cdeb8ac684f'
>>> my_decrypted_md5 = dec.text_decrypt(hash='64c823fad1d87e0df1ef3cdeb8ac684f', word='unsafe', hash_method='MD5')
>>> my_decrypted_md5
True
>>> my_decrypted_md5 = dec.text_decrypt(hash='64c823fad1d87e0df1ef3cdeb8ac684f', word='ahur4', hash_method='MD5')
>>> my_decrypted_md5
False
>>> my_decrypted_md5 = dec.text_decrypt(hash='64c823fad1d87e0df1ef3cdeb8ac684f', word=['ahur4', 'unsafe', 'mesut'], hash_method='MD5')
>>> my_decrypted_md5
'unsafe'
```
---

> - Collecting Proxies and Check Their Health.
>> Available Protocols:
>> - HTTP, SOCKS4, SOCKS5
>
>> p.s : you can also use wrapper function without any argument(default protocol is "http" and default max_ping is 200)

```python

>>> from unsafe import Proxy
>>> proxy = Proxy()
>>> my_proxy_dict = proxy.wrapper(protocol='http', max_ping=200)
>>> my_proxy_dict
{'ip':'port', 'ip':'port', ...}
>>> check_proxy = proxy.checker(proxy_host='127.0.0.1', proxy_port='80', protocol='http', timeout=10)
>>> check_proxy
True
```
---

> - Find Admin Panel.
>> Available Extentions:
>> - php, html, asp, aspx, js, cfm, cgi, brf, slash
>
>> p.s : if use slash for ext argument, function start scanning with this type routes : /admin/ or /login/
>>
>> p.s : all arguments are optional except domain.
```python

>>> from unsafe import BruteForcer
>>> brute = BruteForcer()
>>> founded_logins = brute.admin_finder(domain='example.com', timeout=10, ext='php', user_agent="AmigaVoyager/2.95 (compatible; MC680x0; AmigaOS; SV1)", proxy="http://127.0.0.1:80")
>>> founded_logins
['http://example.com/wp-login.php']

```

> - Find FileManager of Site.
```python

>>> from unsafe import BruteForcer
>>> brute = BruteForcer()
>>> brute.filemanager_finder("example.com", timeout=10)
['https://example.com/filemanager/', 'https://example.com/filemanager/index.php']
```

> - CloudFlare Bypassing.
>> p.s : default "workers" is 5.
```python

>>> from unsafe import BruteForcer
>>> brute = BruteForcer()
>>> brute.cloudflare_bypasser("google.com", workers=10)
{'ns4.google.com': '216.239.38.10', 'search.google.com': '142.251.39.14', 'dns.google.com': '74.91.29.203', 'chat.google.com': '50.7.132.142', 'sites.google.com': '74.91.29.204', 'ads.google.com': '208.110.86.66', 'wap.google.com': '142.251.39.14'}
```
---

> - Find Wordpress Plugins and Extract Users.
>> p.s : all arguments are optional except domain
```python

>>> from unsafe import Wordpress
>>> wp = Wordpress()
>>> #get wordpress users
>>> users = wp.get_user(domain='example.com')
>>> users
['admin', 'administrator']
>>> #max workers count is 5(for now) and default workers count is 3
>>> plugins = wp.plugin_scanner(domain="example.com", timeout=5, workers=5, proxy="http://127.0.0.1:80")
>>> plugins
['http://example.com/wp-content/plugins/wordpress-seo/', 'http://example.com/wp-content/plugins/duplicate-post/', 'http://example.com/wp-content/plugins/w3-total-cache/', 'http://example.com/wp-content/plugins/redirection/', 'http://example.com/wp-content/plugins/favicon-by-realfavicongenerator/']

```
---

> - Show, Delete and Edit Exif Metadata of Image.
```python
>>> from unsafe import ExifImage
>>>
>>> exif = ExifImage()
>>> 
>>> exif.delete_exif_img('/path/of/file.jpg')
True
>>> exif.edit_exif_image('/path/of/file.jpg',key='model', value='unsafe')
True
>>> exif.extract_exif_img('/path/of/file.jpg')
{"make": "huawei", "model": "G-750", ...}
```
---

> - Detect and Cover Faces for Security
>
>> p.s : also you can use your dataset for detect faces in "casc_path" argument(Optional)
```python
>>> from unsafe import Anonymous
>>> a = Anonymous()
>>>
>>> a.anon_picture('path/of/picture.jpg')
"anon_picture_cache/QJA76FH.jpg"
```
---