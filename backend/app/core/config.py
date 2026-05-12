from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/content_factory"
    SECRET_KEY: str  # must be set via .env
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    YOUTUBE_API_KEY: str = ""
    SUPADATA_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    HEYGEN_API_KEY: str = ""
    CREATOMATE_API_KEY: str = ""
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""


settings = Settings()
