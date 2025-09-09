from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')


class KafkaSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='KAFKA_')
    server: str
    server_port: int


class TelegramSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='TELEGRAM_')
    bot_token: SecretStr
    bot_webhook: str


class Settings(BaseConfig):
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)
    telegram: TelegramSettings = Field(default_factory=TelegramSettings)

    @classmethod
    def load(cls):
        return cls()