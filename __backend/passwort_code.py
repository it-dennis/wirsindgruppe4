import hashlib


def encrypt_128(passwort: str) -> str:
    hash_object = hashlib.md5(passwort.enconde())
    encrypted = hash_object.hexdigets()
    return encrypted
