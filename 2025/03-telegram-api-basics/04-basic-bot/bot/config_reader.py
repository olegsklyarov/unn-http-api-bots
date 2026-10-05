from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    telegram_token: SecretStr
    model_config = SettingsConfigDict(env_file=".env")


env_config = Settings()
