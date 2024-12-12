import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str 
    DB_NAME: str
    REDIS_URL: str 
    AVAILABLE_SEATS: int = 10
    LOCK_TIMEOUT: int = 10 
    SERVICE_TIME_PER_PERSON: int = 3  

    class Config:
         env_file = ".env" if os.getenv("ENV") != "test" else ".env.test"

settings = Settings()
