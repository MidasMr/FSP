from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    TESTS_RUN: bool = False
    TEST_DATABASE_URL: str = 'sqlite:///:memory:'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
