import datetime

from jose import jwt


class JwtManager:
    def __init__(
        self, 
        secret_key: str, 
        algorithm: str,
        access_lifetime_sec: int,
        refresh_lifetime_sec: int
    ):
        self.__secret_key = secret_key
        self.__algorithm = algorithm
        self.__access_lifetime = datetime.timedelta(
            seconds=access_lifetime_sec,
        )
        self.__refresh_lifetime = datetime.timedelta(
            seconds=refresh_lifetime_sec,
        )
    

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
            algorithm=self.__algorithm,
            key=self.__secret_key,
        )
    

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self.__secret_key, self.__algorithm)
    

    def create_access_token(
        self,
        user_id: int,
        now: datetime.datetime,
        payload: dict = None,
    ) -> str:
        return self.__create_token(
            user_id=user_id,
            now=now,
            lifetime=self.__access_lifetime,
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
            lifetime=self.__refresh_lifetime,
        )
