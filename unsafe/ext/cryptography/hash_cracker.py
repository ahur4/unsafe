import concurrent.futures
import hashlib
from enum import Enum
from queue import Queue

from unsafe.strings.wordlist import wordlist


class HashTypes(str, Enum):
    SHA1 = 'SHA1'
    SHA224 = 'SHA224'
    SHA256 = 'SHA256'
    SHA384 = 'SHA384'
    SHA512 = 'SHA512'
    SHA3_224 = 'SHA3_224'
    SHA3_256 = 'SHA3_256'
    SHA3_384 = 'SHA3_384'
    SHA3_512 = 'SHA3_512'
    SHAKE128 = 'SHAKE128'
    SHAKE256 = 'SHAKE256'
    MD5 = 'MD5'


def __cracker(data_queue: Queue, hashed: str, hash_type: HashTypes) -> str:
    if not isinstance(hash_type, HashTypes):
        raise TypeError('This Hash Method Not Available !')
    while not data_queue.empty():
        data = data_queue.get()
        data_queue.task_done()
        if hash_type == HashTypes.MD5:
            if hashlib.md5(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHA1:
            if hashlib.sha1(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHA256:
            if hashlib.sha256(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHA224:
            if hashlib.sha224(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHA384:
            if hashlib.sha384(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHA512:
            if hashlib.sha512(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHA3_224:
            if hashlib.sha3_224(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHA3_256:
            if hashlib.sha3_256(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHA3_384:
            if hashlib.sha3_384(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHA3_512:
            if hashlib.sha3_512(data.encode()).hexdigest() == hashed:
                return data
        elif hash_type == HashTypes.SHAKE128:
            if hashlib.shake_128(data.encode()).hexdigest(len(data)) == hashed:
                return data
        elif hash_type == HashTypes.SHAKE256:
            if hashlib.shake_256(data.encode()).hexdigest(len(data)) == hashed:
                return data


def hash_cracker(hashed: str, hash_type: HashTypes, pass_list: list = wordlist, worker: int = 5) -> str:
    if not isinstance(hash_type, HashTypes):
        raise TypeError('This Hash Method Not Available !')
    data_queue: Queue = Queue()
    for password in pass_list:
        data_queue.put(password)
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = []
        for _ in range(worker):
            process = executor.submit(__cracker, data_queue, hashed, hash_type)
            futures.append(process)
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not None:
                return res


if __name__ == '__main__':
    print(hash_cracker(hashed="5d41402abc4b2a76b9719d911017c592", hash_type=HashTypes.MD5))
