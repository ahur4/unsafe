![PyPI](https://img.shields.io/pypi/v/unsafe)
# Unsafe (Advanced Pentesting Module)
An Advanced Module for Penetration Testing.
Using This Module, You Can Implement Brute Force Operations and Identification and Anonymity.
This Module is Always Being Developed and There is No Need to Worry About it Becoming Unavailable.
- Author : Ahur4
- Maintainer : MesutFD

# Features
- [x] [Encrypt and Decrypt Hashs and Encodes](https://github.com/ahur4/unsafe#encrypt-and-decrypt-hashs-and-encodes)
- [x] [Collecting Proxies and Check Their Health](https://github.com/ahur4/unsafe#collecting-proxies-and-check-their-health)
- [x] [BruteForcing Part for Find Admin Panel or FileManager or CloudFlare Bypassing ...](https://github.com/ahur4/unsafe#bruteforcing-part-for-find-admin-panel-or-filemanager-or-cloudflare-bypassing)
- [x] [Show, Delete and Edit Exif Metadata of Image](https://github.com/ahur4/unsafe#show-delete-and-edit-exif-metadata-of-image)
- [x] [All the operations that can be done on WordPress are placed in this section](https://github.com/ahur4/unsafe#all-the-operations-that-can-be-done-on-wordpress-are-placed-in-this-section)
- [x] [Measures to Remain Anonymous](https://github.com/ahur4/unsafe#measures-to-remain-anonymous)
- [x] [Search in Browsers(google_dorking or ...)](https://github.com/ahur4/unsafe#search-in-browsers-google_dorking-or)

# Usage
- #### Encrypt and Decrypt Hashs and Encodes
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
- #### Collecting Proxies and Check Their Health.
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
        from unsafe import Unsafe
        unsafe = Unsafe()

        isActive = unsafe.proxy_checker(proxy_host='127.0.0.1', proxy_port='80', protocol='http', timeout=10)
        print(isActive) # Output : True|False
    ```
---
- #### BruteForcing Part for Find Admin Panel or FileManager or CloudFlare Bypassing ...
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
        from unsafe import Unsafe
        unsafe = Unsafe()

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
        from unsafe import Unsafe
        unsafe = Unsafe()

        realip = unsafe.cloudflare_bypasser(domain='google.com',
                                           workers=5, #Threads
                                        )
        print(realip) # Output : {'ns4.google.com': '216.239.38.10', 'search.google.com': '142.251.39.14', ....}
    ```
---
- #### Show, Delete and Edit Exif Metadata of Image.
    - **Delete Metadata Usage**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        isDeleted = unsafe.delete_exif_img('/path/of/file.jpg')
        print(isDeleted) # Output : True|False
    ```
    - **Edit Metadata Usage**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        isEdited = unsafe.edit_exif_img('/path/of/file.jpg',key='model', value='unsafe')
        print(isEdited) # Output : True|False
    ```
    - **Extract Metadata Usage**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        Exifed = unsafe.extract_exif_img('/path/of/file.jpg')
        print(Exifed) # Output : {"make": "huawei", "model": "G-750", ...}
    ```
---
- #### All the operations that can be done on WordPress are placed in this section.
    - **Extract Admin Users**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        site_users = unsafe.wp_get_users(domain="wordpress.org")
        print(site_users) # Output : ['admin', 'administrator']
    ```
    - **Plugin Scanner**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        site_users = unsafe.wp_plugin_scanner(domain="wordpress.org",
                                              timeout=10,
                                              workers=5,
                                              proxy="http://127.0.0.1:80"
                                            )
        print(site_users) # Output : ['http://wordpress.org/wp-content/plugins/wordpress-seo/',....]
    ```
---
- #### Measures to Remain Anonymous
    - **Detect and Cover Faces**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        result_path = unsafe.anon_picture(image_path="path/of/image.jpg")
        print(result_path) # Output : 'anon_picture_cache/UPW5X51.jpg'
    ```
---
- #### Search in Browsers(google_dorking or ...)
    - **Google Dorking**
    ```python
        from unsafe import Unsafe
        unsafe = Unsafe()

        # Search a Username in Insatgram
        result = unsafe.google_dorking(query='"username" site:insatgram.com')

        print(result) # Output : ['https://instagram.com/username', ....]
    ```
---
# New Features : Coming Soon...