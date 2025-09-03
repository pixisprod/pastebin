from passlib.context import CryptContext

def get_bcrypt_hasher() -> CryptContext:
    return CryptContext(['bcrypt'], deprecated='auto')