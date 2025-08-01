from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class DatabaseSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='DB_')
    host: str
    user: SecretStr
    password: SecretStr
    name: str

class KafkaSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='KAFKA_')
    server: str

class Settings(BaseConfig):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)

    @classmethod
    def load(cls):
        return cls()