from unsafe import cryptography

_hash = 'ada3e80e34da70c99c1acff7f492993c'

cracker = cryptography.hash_cracker(
    hashed=_hash,
    hash_type=cryptography.HashTypes.MD5,
    worker=20,
    pass_list=[
        "Iran",
        "Unsafe",
        "Ahur4",
        "ahur4",
    ]
)

print(f"Hash Cracked :{cracker}" if cracker else "Hash Not Found in PassList.")