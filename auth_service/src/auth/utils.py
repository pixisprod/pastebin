from src.auth.service import AuthService
from src.auth.security.bcrypt import get_bcrypt_hasher
from src.database.UserDAO import UserDAO
        

def setup_auth_service():
    service = AuthService(UserDAO(), get_bcrypt_hasher())
    return service