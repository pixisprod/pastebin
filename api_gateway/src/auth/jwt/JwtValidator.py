from jose import jwt

from src.config import Settings


config = Settings.load()


class JwtValidator:
    def decode_token(self, token: str) -> int:
        return jwt.decode(
            token=token, 
            key=config.jwt.secret_key.get_secret_value(),
            algorithms=['HS256'],
        ).get('sub')
    
    @classmethod
    def load(cls):
        return cls()
