import hashlib


def encrypt(password: str):
    return hashlib.md5(password.encode()).hexdigest()


def verify(plain_password: str, encrypted_password: str):
    return encrypt(plain_password) == encrypted_password
