from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class KafkaConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='KAFKA_')
    bootstrap_server: str


class JwtConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='JWT_')
    secret_key: SecretStr


class ServiceSettings(BaseConfig):
    url: str
    api_ver: str

class AuthServiceSettings(ServiceSettings):
    model_config = SettingsConfigDict(env_prefix='AUTH_SERVICE_')

class PasteServiceSettings(ServiceSettings):
    model_config = SettingsConfigDict(env_prefix='PASTE_SERVICE_')

class Settings(BaseConfig):
    kafka: KafkaConfig = Field(default_factory=KafkaConfig)
    jwt: JwtConfig = Field(default_factory=JwtConfig)
    paste_service: PasteServiceSettings = Field(default_factory=PasteServiceSettings)
    auth_service: AuthServiceSettings = Field(default_factory=AuthServiceSettings)

    @classmethod
    def load(cls):
        return cls()
