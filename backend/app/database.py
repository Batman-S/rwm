from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from app.config import settings
import logging
from typing import Optional, AsyncGenerator

logger = logging.getLogger("DB")

class MongoDBManager:
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._db_name = db_name
        self._client: Optional[AsyncIOMotorClient] = None
        self._db = None

    async def connect(self) -> None:
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
            logger.info("DB connection closed.")

    def get_collection(self, name: str) -> Collection:
        if not self._db:
            raise RuntimeError("Database is not initialized")
        return self._db[name]

db_manager = MongoDBManager(uri=settings.MONGO_URI, db_name=settings.DB_NAME)

# Dependency injections
async def get_mongo_client() -> AsyncGenerator[AsyncIOMotorClient, None]:
    await db_manager.connect()
    try:
        yield db_manager._client
    finally:
        await db_manager.close()

async def get_collection(collection_name: str) -> Collection:
    return db_manager.get_collection(collection_name)
