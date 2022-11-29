# unsafe

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Ahur4, MesutFD (™) 2022

## Examples of How To Use (Buggy Alpha Version)

* Hashing a Text with Different Methods

```python

from unsafe import Encryptor

enc = Encryptor()

#all arguments except words are optional
#hash a text
my_md5 = enc.text_encrypt(words='YOUR WORD TO HASH', encode='UTF-8', hash_method='MD5')
my_shake128 = enc.text_encrypt(words='YOUR WORD TO HASH', encode='UTF-8', hash_method='SHAKE128', count = 22)
my_base64 = enc.text_encrypt(words='YOUR WORD TO HASH', encode='UTF-8', hash_method='BASE64')

#hash a file
my_md5_file = enc.file_encrypt(filename='unsafe.txt', encode='UTF-8', hash_method='MD5')
```

* Collecting Proxies and Check Their Health.

```python

from unsafe import Proxy

proxy = Proxy()

my_proxy_dict = proxy.wrapper(protocol='http', max_ping=200)
check_proxy = proxy.checker(proxy_host='127.0.0.1', proxy_port='80', protocol='http', timeout=10)
```

