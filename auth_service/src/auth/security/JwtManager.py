import datetime

from jose import jwt

from src.config import Settings


config = Settings.load()


class JwtManager:
    def __create_token(
        self,
        user_id: int,
        now: datetime.datetime,
        lifetime: datetime.timedelta,
        payload: dict = None,
    ) -> str:
        temp_payload = {
            'sub': str(user_id),
            'iat': int(now.timestamp()),
            'exp': int((now + lifetime).timestamp()),
        }
        if payload:
            temp_payload.update(payload)
        return jwt.encode(
            claims=temp_payload,
            algorithm='HS256',
            key=config.jwt.secret_key.get_secret_value()
        )
    
    def create_access_token(
        self,
        user_id: int,
        now: datetime.datetime,
        payload: dict = None,
    ) -> str:
        return self.__create_token(
            user_id=user_id,
            now=now,
            lifetime=datetime.timedelta(seconds=config.jwt.access_token_lifetime_seconds),
            payload=payload,
        )
    
    def create_refresh_token(
        self,
        user_id: int,
        now: datetime.datetime,
    ) -> str:
        return self.__create_token(
            user_id=user_id,
            now=now,
            lifetime=datetime.timedelta(seconds=config.jwt.refresh_token_lifetime_seconds)
        )
    
    @classmethod
    def load(cls):
        return cls()