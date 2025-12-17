from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_URL: str
    API_KEY: str
    API_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()