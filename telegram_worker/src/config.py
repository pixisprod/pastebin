from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')


class KafkaSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='KAFKA_')
    server: str
    server_port: int


class Settings(BaseConfig):
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)

    @classmethod
    def load(cls):
        return cls()