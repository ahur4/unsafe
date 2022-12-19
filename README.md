![PyPI](https://img.shields.io/pypi/v/unsafe)
# Unsafe (Advanced Pentesting Module)
An Advanced Module for Penetration Testing.
Using This Module, You Can Implement Brute Force Operations and Identification and Anonymity.
This Module is Always Being Developed and There is No Need to Worry About it Becoming Unavailable.
- Author : Ahur4
- Maintainer : MesutFD


# Usage
- **Encrypt and Decrypt Hashs and Encodes**
    - **Available Methods:**

        ( md5 | sha1 | sha224 | sha256 | sha384 | sha512 | sha3-224 | sha3-256 \
        sha3-384 | sha3-512 | shake128 | shake256 | base16 | base32 | base64 \
        base85 | ascii85 | caesar )

    - **Encryption** :
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
    - **Decryption** :
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
