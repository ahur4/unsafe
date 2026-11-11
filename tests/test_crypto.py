"""Round-trips for the encoding and digest helpers."""

import hashlib

import pytest

from unsafe import cryptography


def test_encodings_round_trip():
    text = "Ahur4 caf\u00e9"
    pairs = (
        (cryptography.encrypt_base64, cryptography.decrypt_base64),
        (cryptography.encrypt_base32, cryptography.decrypt_base32),
        (cryptography.encrypt_base16, cryptography.decrypt_base16),
        (cryptography.encrypt_base85, cryptography.decrypt_base85),
        (cryptography.encrypt_ascii85, cryptography.decrypt_ascii85),
    )
    for encrypt, decrypt in pairs:
        assert decrypt(encrypt(text)) == text


def test_caesar_default_matches_and_rejects_bad_keys():
    encrypted = cryptography.encrypt_caesar("Abc xyz!")
    assert encrypted == "Fgh cde!"
    assert cryptography.decrypt_caesar(encrypted) == "Abc xyz!"
    assert cryptography.decrypt_caesar(cryptography.encrypt_caesar("Z", 1), 1) == "Z"
    for pointer in (0, 27, -1):
        with pytest.raises(ValueError):
            cryptography.encrypt_caesar("A", pointer)
        with pytest.raises(ValueError):
            cryptography.decrypt_caesar("A", pointer)


def test_digest_vectors():
    assert cryptography.hash_md5("") == "d41d8cd98f00b204e9800998ecf8427e"
    assert cryptography.hash_sha256("abc") == hashlib.sha256(b"abc").hexdigest()
    assert cryptography.hash_sha1("abc") == hashlib.sha1(b"abc").hexdigest()
    assert cryptography.hash_sha224("abc") == hashlib.sha224(b"abc").hexdigest()
    assert cryptography.hash_sha384("abc") == hashlib.sha384(b"abc").hexdigest()
    assert cryptography.hash_sha512("abc") == hashlib.sha512(b"abc").hexdigest()
    assert cryptography.hash_sha3_224("abc") == hashlib.sha3_224(b"abc").hexdigest()
    assert cryptography.hash_sha3_256("abc") == hashlib.sha3_256(b"abc").hexdigest()
    assert cryptography.hash_sha3_384("abc") == hashlib.sha3_384(b"abc").hexdigest()
    assert cryptography.hash_sha3_512("abc") == hashlib.sha3_512(b"abc").hexdigest()
    assert cryptography.hash_shake128("abc", 8) == hashlib.shake_128(b"abc").hexdigest(8)
    assert cryptography.hash_shake256("abc", 16) == hashlib.shake_256(b"abc").hexdigest(16)
