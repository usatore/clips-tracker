from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    YOUTUBE_API_KEY: str

    INSTAGRAM_USERNAME: str
    INSTAGRAM_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()