from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class DatabaseSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='DB_')
    host: str
    user: SecretStr
    password: SecretStr
    name: str

class JwtSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='JWT_')
    secret_key: SecretStr
    algorithm: str
    refresh_token_cookie_name: str
    access_token_lifetime_seconds: int
    refresh_token_lifetime_seconds: int


class KafkaSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='KAFKA_')
    server: str


class AvroSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='AVRO_')
    SR_server: str


class AppSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='APP_')
    service_state_key: str



class Settings(BaseConfig):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    jwt: JwtSettings = Field(default_factory=JwtSettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)
    avro: AvroSettings = Field(default_factory=AvroSettings)
    app: AppSettings = Field(default_factory=AppSettings)

    @classmethod
    def load(cls):
        return cls()