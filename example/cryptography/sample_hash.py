from unsafe import cryptography

keyword = "Ahur4"

_hash = cryptography.hash_md5(text=keyword)

print(keyword, "Hashed (MD5):", _hash)