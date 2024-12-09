import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str 
    DB_NAME: str

    class Config:
         env_file = ".env" if os.getenv("ENV") != "test" else ".env.test"

settings = Settings()
