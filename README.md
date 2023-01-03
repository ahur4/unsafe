![PyPI](https://img.shields.io/pypi/v/unsafe)
![Downloads](https://static.pepy.tech/personalized-badge/unsafe?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)
![Downloads](https://static.pepy.tech/personalized-badge/unsafe?period=month&units=none&left_color=grey&right_color=blue&left_text=Downloads)
![Downloads](https://static.pepy.tech/personalized-badge/unsafe?period=week&units=none&left_color=grey&right_color=blue&left_text=Downloads)
![GitHub repo size](https://img.shields.io/github/repo-size/ahur4/unsafe?label=size)
![PyPI - License](https://img.shields.io/pypi/l/unsafe)
![Telegram-Channel](https://ExploitPriv8)
# Unsafe (Advanced Penetration Testing Module)
An Advanced Module for Penetration Testing.
Using This Module, You Can Implement Brute Force Operations and Identification and Anonymity.
This Module is Always Being Developed and There is No Need to Worry About it Becoming Unavailable.
- Author : Ahur4
    - 𝗘 𝗫 𝗣 𝗟 𝗢 𝗜 𝗧 : [Telegram Channel](https://t.me/ExploitPriv8)
- Maintainer : MesutFD



# Features
- [x] [Encryption & Decryption](https://github.com/ahur4/unsafe#usage)
- [x] [Proxy](https://github.com/ahur4/unsafe#proxy)
- [x] [BruteForce](https://github.com/ahur4/unsafe#bruteforce)
- [x] [Forensic](https://github.com/ahur4/unsafe#forensic)
- [x] [Wordpress](https://github.com/ahur4/unsafe#wordpress)
- [x] [VulnerabilityScanner](https://github.com/ahur4/unsafe#vulnerabilityscanner)
- [x] [Crawling.](https://github.com/ahur4/unsafe#crawling)
- [x] [Network.](https://github.com/ahur4/unsafe#network)


# Usage
- #### Encryption & Decryption
    - **Available Methods:**

        ( md5 | sha1 | sha224 | sha256 | sha384 | sha512 | sha3-224 | sha3-256 \
        sha3-384 | sha3-512 | shake128 | shake256 | base16 | base32 | base64 \
        base85 | ascii85 | caesar )

    - **Encryption Usage** :
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()
    
        name = "Ahur4"
    
        md5_name = unsafe.text_encrypt(name) #Default hash_method is "md5"
        print(md5_name) #Output : 'ada3e80e34da70c99c1acff7f492993c'
    
        base64_name = unsafe.text_encrypt(name, hash_method="base64")
        print(base64_name) #Output : b'QWh1cjQ='
    
        caesar_name = unsafe.text_encrypt(name, hash_method="caesar", count=5)
        print(caesar_name) #Output : 'Fmzw4'
    
        shake128_name = unsafe.text_encrypt(name, encode='UTF-8', hash_method="shake128", count=15)
        print(shake128_name) #Output : ''c8a3ab8ca74720d227550f4f76b71f''
    
    ```
    - **Decryption Usage** :
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        hash = "ada3e80e34da70c99c1acff7f492993c" #Md5 - Value : Ahur4

        name = unsafe.text_decrypt(hash=hash, word="Ahur4") #Default hash_method is "md5"
        print(name) #Output : True

        # When Do Not Have any Word or Wordlist Default Wordlist is John The Ripper Wordlist
        name = unsafe.text_decrypt(hash=hash, hash_method="sha1")
        print(name) #Output : '' ,Cause Not Found Result.

    ```
---
- #### Proxy
    - **Available Protocols** :

        (http | socks4 | socks5)
    - **Proxy Wrapper Usage**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        proxies = unsafe.proxy_wrapper(protocol="http", max_ping=200)
        print(proxies) # Output : {'ip':'port', 'ip':'port', ...}
    ```
    - **Proxy Checker Usage**
    ```python
        isActive = unsafe.proxy_checker(proxy_host='127.0.0.1', proxy_port='80', protocol='http', timeout=10)
        print(isActive) # Output : True|False
    ```
---
- #### BruteForce
    - **AdminFinder Usage**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        admin_panels = unsafe.admin_finder(domain='example.com',
                                           workers=5, #Threads
                                           timeout=10,
                                           ext='php', #Site type
                                           user_agent="AmigaVoyager/2.95 (compatible; MC680x0; AmigaOS; SV1)",
                                           proxy="http://127.0.0.1:80"
                                        )
        print(admin_panels) # Output : ['http://example.com/wp-login.php']
    ```
    - **FileManager Finder Usage**
    ```python
        filemanagers = unsafe.filemanager_finder(domain='example.com',
                                           workers=5, #Threads
                                           timeout=10,
                                           user_agent="AmigaVoyager/2.95 (compatible; MC680x0; AmigaOS; SV1)",
                                           proxy="http://127.0.0.1:80"
                                        )
        print(filemanagers) # Output : ['https://example.com/filemanager/', 'https://example.com/filemanager/index.php']
    ```
    - **CloudFlare Bypassing Usage**
    ```python
        realip = unsafe.cloudflare_bypasser(domain='google.com',
                                           workers=5, #Threads
                                        )
        print(realip) # Output : {'ns4.google.com': '216.239.38.10', 'search.google.com': '142.251.39.14', ....}
    ```
    - **SubDomain Finder**
    ```python
        result = unsafe.subdomain_scanner(
            domain="google.com",
            workers=5,
            subdomains=["ww1", "forum", "download", "product", "search", "cdn", "ns1"], #Also this part have a default subdomains list.
            timeout=5,
            proxy="http://127.0.0.1:80"
            )
        print(result) # Output : ["ww1.google.com", ...]
    ```
---
- #### Forensic.
    - **Delete Image Metadata Usage**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        isDeleted = unsafe.delete_exif_img(path='/path/of/file.jpg')
        print(isDeleted) # Output : True|False
    ```
    - **Edit Image Metadata Usage**
    ```python
        isEdited = unsafe.edit_exif_img(path='/path/of/file.jpg',key='model', value='unsafe')
        print(isEdited) # Output : True|False
    ```
    - **Extract Image Metadata Usage**
    ```python
        Exifed = unsafe.extract_exif_img(path='/path/of/file.jpg')
        print(Exifed) # Output : {"make": "huawei", "model": "G-750", ...}
    ```
    - **Delete PDF Metadata Usage**
    ```python
        result = unsafe.remove_pdf_metadata(filename="path/of/file.pdf")
        print(result) # Output : 'path/of/output.pdf'
    ```
    - **Edit PDF Metadata Usage**
    ```python
        result = unsafe.edit_pdf_metadata(filename="path/of/file.pdf", metadata={"unsafe":"module"})
        print(result) # Output : 'path/of/output.pdf'
    ```
    - **Extract PDF Metadata Usage**
    ```python
        result = unsafe.get_pdf_metadata(filename="path/of/file.pdf")
        print(result) # Output : {"/data":"values",...}
    ```
    - **Delete Audio Metadata Usage**
    ```python
        result = unsafe.remove_audio_metadata(filename="path/of/file.mp3")
        print(result) # Output : 'path/of/output.mp3'
    ```
    - **Edit Audio Metadata Usage**
    ```python
        result = unsafe.edit_audio_metadata(filename="path/of/file.mp3", metadata={"artist": "Ahur4"})
        print(result) # Output : 'path/of/output.mp3'
    ```
    - **Extract Audio Metadata Usage**
    ```python
        result = unsafe.get_audio_metadata(filename="path/of/file.mp3")
        print(result) # Output : # Output : {"/data":"values",...}
    ```
---
- #### Wordpress.
    - **Extract Admin Users**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        site_users = unsafe.wp_get_users(domain="wordpress.org")
        print(site_users) # Output : ['admin', 'administrator']
    ```
    - **Plugin Scanner**
    ```python
        site_users = unsafe.wp_plugin_scanner(domain="wordpress.org",
                                              timeout=10,
                                              workers=5,
                                              proxy="http://127.0.0.1:80"
                                            )
        print(site_users) # Output : ['http://wordpress.org/wp-content/plugins/wordpress-seo/',....]
    ```
---
- #### VulnerabilityScanner
    - **Xss Vulnerability Scanner**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        result = unsafe.xss_scanner(url="https://example.com/news.php", js_script="<Script>alert('hi')</scripT>")
        print(result) # Output : {"is_vulnerable": is_vulnerable, "form_detail": form_details}
    ```
    - **SqlInjection Vulnerability Scanner**
    ```python
        result = unsafe.sql_injection_scanner(url="https://example.com/news.php?id=475433")
        print(result) # Output : ["https://example.com/news.php?id=245", "......", ..]
    ```
- #### Crawling.
    - **Crawling a single Page and Extract Usernames, Phones, Emails and ...**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        result = unsafe.crawl_single_page(url="https://example.com/contact.php", timeout=5, proxy="http://127.0.0.1:80")
        print(result) #Output : {"links": [...], "phones": [...], ...}
    ```
    - **Search in Three Search Engines: Google, Bing and Ask**
    ```python
        # Search a Username in Insatgram
        result = unsafe.browser_search(query='"username" site:insatgram.com', timeout=10, proxy="http://127.0.0.1:80")
        print(result) # Output : ['https://instagram.com/username', ....]
    ```
    - **Scan Entered Page and Detect Xss Vulnerability.**
    ```python
        result = unsafe.xss_scanner(url="https://xsslabs.com/xss-labs-1.php", js_script="<Script>alert('hi')</scripT>")
        print(result) # Output : {'is_vulnerable': True, 'form_detail': {'action': '#', 'method': 'get', 'inputs': [{'type': 'text', 'name': 'name', 'value': "<Script>alert('hi')</scripT>"}]}}
    ```
---
- #### Network
    - **Scan Open Ports.**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        result = unsafe.port_scanner(host="127.0.0.1", ports=[80, 53, 443, 127])
        print(result) # Output : [80, 443]
    ```
    - **Mac Address Lookup(find owner of device company)**
    ```python
        result = unsafe.mac_address_lookup(mac="00:00:5e:00:53:af")
        print(result) #Output : "U.S. Department of Defense (IANA)"
    ```
# New Features : Coming Soon...