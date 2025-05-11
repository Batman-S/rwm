from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger("DB")


class MongoDBManager:
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._db_name = db_name
        self._client: Optional[AsyncIOMotorClient] = None
        self._db = None

    async def connect(self) -> None:
        if not self._client:
            try:
                self._client = AsyncIOMotorClient(self._uri)
                self._db = self._client[self._db_name]
                logger.info(f"Connected to {self._uri}, Database: {self._db_name}")
            except Exception as e:
                logger.error(f"Failed to connect to DB: {str(e)}")
                raise RuntimeError("Failed to connect to DB") from e

    async def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("DB connection closed.")

    def get_collection(self, name: str) -> Collection:
        if self._db is None:
            raise RuntimeError("Database is not initialized")
        return self._db[name]


db_manager = MongoDBManager(uri=settings.MONGO_URI, db_name=settings.DB_NAME)


# Dependency injections
async def get_collection(collection_name: str) -> Collection:
    return db_manager.get_collection(collection_name)
