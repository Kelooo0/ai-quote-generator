from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    LLM_PROVIDER: str = "mock"
    MODEL: str = "gpt-5.6-luna"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
