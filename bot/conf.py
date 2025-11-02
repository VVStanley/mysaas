from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    API_TOKEN: str
    SAAS_API_URL: str = "http://django:8000/api"


settings = Settings()
