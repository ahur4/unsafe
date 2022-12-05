from typing import Union
import base64
import hashlib
from unsafe.exceptions import UnknownEncoding


class Encryptor:
    """
    This is a Class for Text/File Encryption.
    """

    def __init__(self) -> None:
        pass

    def text_encrypt(self, words: str, encode: str | None = None, hash_method: str = 'MD5', **kwargs: str):
        """
        function to return encrypted string.
        
        args:

            * words: your words to hash
            
            `text_encrypt(words = "hello world")`
            
            * encode: your choose to encode(default=None)
            
            `text_encrypt(words = "hello world", encode = "UTF-8")`
            
            * hash_method: your chosen hash method(default=md5)
            
            `text_encrypt(words = "hello world", hash_method = "SHA1")`
            
            `Available Hash Method's : ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512', 'SHA3-224', 'SHA3-256', 'SHA3-384', 'SHA3-512', 'SHAKE128', 'SHAKE256', 'BASE16', 'BASE32', 'BASE64', 'BASE85', 'ASCII85', 'CAESAR']`

            * count: for 'SHAKE128', 'SHAKE256' and 'CAESAR' method's(default for shake methods = 15 AND default for caesar method = 1)
            
            `text_encrypt(words = "hello world", hash_method = 'SHAKE128', count = 22)`
            
            `text_encrypt(words = "hello world", hash_method = 'CAESAR', count = 4)`
        """

        hash_method = hash_method.lower()

        if isinstance(words, Union[int, float, bool]):
            words = str(words)

        if kwargs != {} and hash_method not in ['shake128', 'shake256', 'caesar']:
            raise ValueError('This Hash Method Have Not Kwargs...')

        if kwargs == {} and hash_method in ['shake128', 'shake256']:
            count = 15
        elif kwargs != {} and hash_method in ['shake128', 'shake256']:
            if 'count' in kwargs:
                try:
                    count = int(kwargs['count'])
                except:
                    raise ValueError('count must be integer !')
            else:
                raise ValueError(
                    f'The argument(s) {[i for i in kwargs.keys()]} not defined !')
        elif kwargs == {} and hash_method == 'caesar':
            count = 1
        elif kwargs != {} and hash_method == 'caesar':
            if 'count' in kwargs:
                try:
                    count = int(kwargs['count'])
                except:
                    raise ValueError('count must be integer !')
            else:
                raise ValueError(
                    f'The argument(s) {[i for i in kwargs.keys()]} not defined !')

        if encode and hash_method == 'caesar' or not encode and hash_method == 'caesar':
            pass
        elif encode:
            try:
                if type(words) == bytes:
                    words = words.decode()
                    words = words.encode()
                else:
                    words = words.encode()
            except LookupError:
                raise UnknownEncoding(encode)
            except Exception as e:
                raise e

        else:
            if type(words) == bytes:
                words = words.decode()
                words = words.encode()
            else:
                words = words.encode()
        if hash_method == 'md5':
            return hashlib.md5(words).hexdigest()
        elif hash_method == 'sha1':
            return hashlib.sha1(words).hexdigest()
        elif hash_method == 'sha256':
            return hashlib.sha256(words).hexdigest()
        elif hash_method == 'sha224':
            return hashlib.sha224(words).hexdigest()
        elif hash_method == 'sha384':
            return hashlib.sha384(words).hexdigest()
        elif hash_method == 'sha512':
            return hashlib.sha512(words).hexdigest()
        elif hash_method == 'sha3-224':
            return hashlib.sha3_224(words).hexdigest()
        elif hash_method == 'sha3-256':
            return hashlib.sha3_256(words).hexdigest()
        elif hash_method == 'sha3-384':
            return hashlib.sha3_384(words).hexdigest()
        elif hash_method == 'sha3-512':
            return hashlib.sha3_512(words).hexdigest()
        elif hash_method == 'base85':
            return base64.b85encode(words)
        elif hash_method == 'base64':
            return base64.b64encode(words)
        elif hash_method == 'base32':
            return base64.b32encode(words)
        elif hash_method == 'base16':
            return base64.b16encode(words)
        elif hash_method == 'ascii85':
            return base64.a85encode(words)
        elif hash_method == 'shake128':
            return hashlib.shake_128(words).hexdigest(count)
        elif hash_method == 'shake256':
            return hashlib.shake_256(words).hexdigest(count)
        elif hash_method == 'caesar':
            if (type(count) != int) or (count not in range(1, 27)):
                raise ValueError(
                    "the key must be an integer between: 1 and 26")
            if (not words) or (len(words) == 0):
                raise ValueError("You must provide data")
            abcd = "abcdefghijklmnopqrstuvwxyz"
            ABCD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            hash = ""
            for i in words:
                if str(i) in abcd:
                    hash += abcd[(abcd.index(str(i)) + count) % 26]
                elif str(i) in ABCD:
                    hash += ABCD[(ABCD.index(str(i)) + count) % 26]
                else:
                    hash += str(i)
            return hash
        else:
            raise ValueError('This Hash Method Not Available !')

    def file_encrypt(self, filename: str, encode: str | None = None, hash_method: str = 'MD5',
                     **kwargs: dict[str, int]):
        """
        function to return encrypted string.
        
        args:

            * filename: your filename to hash
            
            `file_encrypt(filename = "path/of/file.text")`
            
            * encode: your choose to encode(default=None)
            
            `file_encrypt(filename = "path/of/file.text", encode = "UTF-8")`
            
            * hash_method: your chosen hash method(default=md5)
            
            `file_encrypt(filename = "path/of/file.text", hash_method = "SHA1")`
            
            `Available Hash Method's : ['MD5', 'SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512', 'SHA3-224', 'SHA3-256', 'SHA3-384', 'SHA3-512', 'SHAKE128', 'SHAKE256', 'BASE16', 'BASE32', 'BASE64', 'BASE85', 'ASCII85']`

            * len_count: for 'SHAKE128' and 'SHAKE256' method's(default=15)
            
            `file_encrypt(filename = "path/of/file.text", hash_method = 'SHAKE128, len_count = 22)`
        """
        try:
            with open(filename, "rb") as f:
                words = f.read()
            f.close()

            if hash_method == 'md5':
                return self.text_encrypt(str(words), encode=encode, hash_method='md5', **kwargs)
            elif hash_method == 'sha1':
                return self.text_encrypt(str(words), encode=encode, hash_method='sha1', **kwargs)
            elif hash_method == 'sha256':
                return self.text_encrypt(str(words), encode=encode, hash_method='sha256', **kwargs)
            elif hash_method == 'sha224':
                return self.text_encrypt(str(words), encode=encode, hash_method='sha224', **kwargs)
            elif hash_method == 'sha384':
                return self.text_encrypt(str(words), encode=encode, hash_method='sha384', **kwargs)
            elif hash_method == 'sha512':
                return self.text_encrypt(str(words), encode=encode, hash_method='sha512', **kwargs)
            elif hash_method == 'sha3-224':
                return self.text_encrypt(str(words), encode=encode, hash_method='sha3-224', **kwargs)
            elif hash_method == 'sha3-256':
                return self.text_encrypt(str(words), encode=encode, hash_method='sha3-256', **kwargs)
            elif hash_method == 'sha3-384':
                return self.text_encrypt(str(words), encode=encode, hash_method='sha3-384', **kwargs)
            elif hash_method == 'sha3-512':
                return self.text_encrypt(str(words), encode=encode, hash_method='sha3-512', **kwargs)
            elif hash_method == 'base85':
                return self.text_encrypt(str(words), encode=encode, hash_method='base85', **kwargs)
            elif hash_method == 'base64':
                return self.text_encrypt(str(words), encode=encode, hash_method='base64', **kwargs)
            elif hash_method == 'base32':
                return self.text_encrypt(str(words), encode=encode, hash_method='base32', **kwargs)
            elif hash_method == 'base16':
                return self.text_encrypt(str(words), encode=encode, hash_method='base16', **kwargs)
            elif hash_method == 'ascii85':
                return self.text_encrypt(str(words), encode=encode, hash_method='ascii85', **kwargs)
            elif hash_method == 'shake128':
                return self.text_encrypt(str(words), encode=encode, hash_method='shake128', **kwargs)
            elif hash_method == 'shake256':
                return self.text_encrypt(str(words), encode=encode, hash_method='shake256', **kwargs)
            else:
                raise ValueError('This Hash Method Not Available !')
        except Exception as e:
            raise e
