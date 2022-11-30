# unsafe

> A practical and optimal library for those interested in Pentest, cryptography,Vulnerability Scanner and ..!
> 
> Developed by Ahur4, MesutFD (™) 2022

## Examples of How To Use.

> - Hashing, Encrypting and Hash Cracking or Text Decryption
>> Available Mathods :
>> - ##### MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SHA3-224, SHA3-256, SHA3-384, SHA3-512, SHAKE128, SHAKE256
>> - ##### BASE16, BASE32, BASE64, BASE64, BASE85, ASCII85, CAESAR
>>> p.s : for shake methods(128, 256) and caesar method you must use count parameter in calling function.
>>>
>>> p.s : in encryption and decryption all arguments are optional except words(in encrypt) and hash(in decrypt).
>>>
>>> p.s : for default wordlist there is John The Ripper's tool wordlist.

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

> - Hash Cracking and Decode a Encrypted Text

```python

>>> from unsafe import Decrypter
>>> dec = Decrypter()

>>> #all arguments except words are optional
>>> #hash a text
>>> my_decrypted_md5 = dec.text_decrypt(hash='28488a21527473bec901c7cc2bfbd76b', words='YOUR WORD TO HASH', hash_method='MD5')
>>> my_decrypted_md5
'YOUR WORD TO HASH'
>>> my_decrypted_shake128 = dec.text_decrypt(hash='5f75455db6b0b3652f20cd6d67972a67746631f3a562', words='Wrong Words', hash_method='SHAKE128')
>>> #return a empty string when encrypted words dont match to hash
>>> my_decrypted_shake128
''
>>> my_decrypted_base64 = dec.text_decrypt(hash=b'WU9VUiBXT1JEIFRPIEhBU0g=', hash_method='BASE64')
>>> my_decrypted_base64
'YOUR WORD TO HASH'
```

> - Collecting Proxies and Check Their Health.

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

> - Find Admin Panel.

```python

>>> from unsafe import BruteForcer
>>> brute = BruteForcer()
>>> a = brute.admin_finder(domain='example.com', timeout=10, ext='php')
>>> a
{'http://example.com': ['http://example.com/wp-login.php']}

```

> - Find Wordpress Plugins and Extract Users.

```python

>>> from unsafe import Wordpress
>>> wp = Wordpress()
>>> #get wordpress users
>>> users = wp.get_user(domain='example.com')
>>> users
['admin', 'administrator']
>>> #max workers count is 5(for now) and default workers count is 3
>>> plugins = wp.plugin_scanner(url="example.com", timeout=5, workers=5, proxy="http://127.0.0.1:80")
>>> plugins
['http://example.com/wp-content/plugins/wordpress-seo/', 'http://example.com/wp-content/plugins/duplicate-post/', 'http://example.com/wp-content/plugins/w3-total-cache/', 'http://example.com/wp-content/plugins/redirection/', 'http://example.com/wp-content/plugins/favicon-by-realfavicongenerator/']

```
