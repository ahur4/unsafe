import base64 as b64
from string import ascii_uppercase, ascii_lowercase


def caesar(keyword: str, pointer: int) -> str:
    if pointer not in range(1, 27):
        raise ValueError("the key must be an integer between: 1 and 26")
    _decoded = ""
    for letter in keyword:
        if letter in ascii_lowercase:
            _decoded += ascii_lowercase[(ascii_lowercase.index(letter) - pointer) % 26]
        elif letter in ascii_uppercase:
            _decoded += ascii_uppercase[(ascii_uppercase.index(letter) - pointer) % 26]
        else:
            _decoded += letter
    return _decoded


def ascii85(text: str) -> str:
    return b64.a85decode(text).decode()


def base16(text: str) -> str:
    return b64.b16decode(text).decode()


def base32(text: str) -> str:
    return b64.b32decode(text).decode()


def base64(text: str) -> str:
    return b64.b64decode(text).decode()


def base85(text: str) -> str:
    return b64.b85decode(text).decode()
