from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    HONEYPOT_API_KEY: str = "your-secret-key"
    GEMINI_API_KEY: Optional[str] = None
    GUVI_CALLBACK_URL: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
