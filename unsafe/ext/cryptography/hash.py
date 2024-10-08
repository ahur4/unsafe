import hashlib


def md5(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha1(text: str) -> str:
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


def sha224(text: str) -> str:
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def sha384(text: str) -> str:
    return hashlib.sha384(text.encode('utf-8')).hexdigest()


def sha512(text: str) -> str:
    return hashlib.sha512(text.encode('utf-8')).hexdigest()


def sha3_224(text: str) -> str:
    return hashlib.sha3_224(text.encode('utf-8')).hexdigest()


def sha3_256(text: str) -> str:
    return hashlib.sha3_256(text.encode('utf-8')).hexdigest()


def sha3_384(text: str) -> str:
    return hashlib.sha3_384(text.encode('utf-8')).hexdigest()


def sha3_512(text: str) -> str:
    return hashlib.sha3_512(text.encode('utf-8')).hexdigest()


def shake128(text: str, length: int = 20) -> str:
    return hashlib.shake_128(text.encode('utf-8')).hexdigest(length)


def shake256(text: str, length: int = 20) -> str:
    return hashlib.shake_256(text.encode('utf-8')).hexdigest(length)
