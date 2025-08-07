from passlib.context import CryptContext

async def get_bcrypt_hasher() -> CryptContext:
    return CryptContext(['bcrypt'], deprecated='auto')