from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    LLM_PROVIDER: str = "mock"
    MODEL: str = "gpt-5.6-luna"
    BASE_DIR: Path = Path(__file__).resolve().parent
    DATA_DIR: Path = BASE_DIR / "data"
    PRICING_FILE: Path = DATA_DIR / "pricing.json"
    COMPANY_DATA_FILE: Path = DATA_DIR / "company_data.json"
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
