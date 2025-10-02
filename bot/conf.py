import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(os.getenv("TELEGRAM_BOT_TOKEN"), env="BOT_TOKEN")
    DJANGO_API_URL: str = "http://django:8000/api/"
    AUTH_TOKEN: str = "123123123"


settings = Settings()
