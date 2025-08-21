from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')


class AvroSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='AVRO_')
    sr_server: str


class Settings(BaseConfig):
    avro: AvroSettings = Field(default_factory=AvroSettings)

    @classmethod
    def load(cls):
        return cls()