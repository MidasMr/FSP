from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOSTNAME: str
    DB_PORT: str
    DB_NAME: str
    TESTS_RUN: bool = False
    TEST_DATABASE_URL: str = 'sqlite:///:memory:'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
