from unsafe import cryptography

keyword = "Ahur4"
encrypted = cryptography.encrypt_ascii85(text=keyword)
print(keyword, "Encrypted:", encrypted)