import base64 as b64
from string import ascii_uppercase, ascii_lowercase


def caesar(keyword: str, pointer: int = 5) -> str:
    if pointer not in range(1, 27):
        raise ValueError("the key must be an integer between: 1 and 26")
    _hash = ""
    for i in keyword:
        if str(i) in ascii_lowercase:
            _hash += ascii_lowercase[(ascii_lowercase.index(str(i)) + pointer) % 26]
        elif str(i) in ascii_uppercase:
            _hash += ascii_uppercase[(ascii_uppercase.index(str(i)) + pointer) % 26]
        else:
            _hash += str(i)
    return _hash


def ascii85(text: str) -> str:
    return b64.a85encode(text.encode()).decode()


def base16(text: str) -> str:
    return b64.b16encode(text.encode()).decode()


def base32(text: str) -> str:
    return b64.b32encode(text.encode()).decode()


def base64(text: str) -> str:
    return b64.b64encode(text.encode()).decode()


def base85(text: str) -> str:
    return b64.b85encode(text.encode()).decode()
