from unsafe import cryptography

_encrypted = '6"kC]1]'
_decrypted = cryptography.decrypt_ascii85(text=_encrypted)
print(_encrypted, "Decrypted :", _decrypted)