from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

from eventhub.avro.AvroManager import AvroManager
from eventhub.confluent.ConfluentSRClient import ConfluentSRClient

from src.auth.AuthService import AuthService
from src.auth.AuthService import ServiceInfra
from src.database.UserDAO import UserDAO
from src.auth.security.JwtManager import JwtManager
from src.auth.security.bcrypt import get_bcrypt_hasher
from src.config import Settings


config = Settings.load()


async def get_jwt_manager():
    manager = JwtManager()
    return manager

jwt_manager_dep = Annotated[JwtManager, Depends(get_jwt_manager)]


async def get_service_infra():
    async with ConfluentSRClient(config.avro.SR_server) as sr:
        avro_manager = AvroManager(sr)
        sr_client = sr
        hasher = await get_bcrypt_hasher()
        yield ServiceInfra(hasher, avro_manager, sr_client)

service_infra_dep = Annotated[ServiceInfra, Depends(get_service_infra)]