from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')


class DatabaseSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='DB_')
    host: str
    user: SecretStr
    password: SecretStr
    name: str


class KafkaSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='KAFKA_')
    server: str


class AppSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='APP_')
    service_state_key: str


class PasteSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='PASTE_')
    content_min_length: int
    content_max_length: int
    lifetime_min_seconds: int
    lifetime_max_seconds: int
    public_url_min_length: int
    public_url_max_length: int


class JwtSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='JWT_')
    secret_key: SecretStr
    algorithm: str


class Settings(BaseConfig):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)
    app: AppSettings = Field(default_factory=AppSettings)
    paste: PasteSettings = Field(default_factory=PasteSettings)
    jwt: JwtSettings = Field(default_factory=JwtSettings)

    @classmethod
    def load(cls):
        return cls()