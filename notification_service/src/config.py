from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr, Field


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')


class DatabaseSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='NOTIFICATION_DB_')
    host: str
    user: SecretStr
    password: SecretStr
    name: str


class KafkaSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='KAFKA_')
    server: str
    server_port: int



class Settings(BaseConfig):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)

    @classmethod
    def load(cls):
        return cls()