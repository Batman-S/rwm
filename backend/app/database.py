from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from app.config import settings
import logging
from typing import Optional

logger = logging.getLogger("DB")

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._db_name = db_name
        self._client: Optional[AsyncIOMotorClient] = None
        self._db = None

    async def connect(self) -> None:
        try:
            self._client = AsyncIOMotorClient(self._uri)
            self._db = self._client[self._db_name]
            logger.info(f"Connected {self._uri}, Database: {self._db_name}")
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

    async def safe_query(self, query_func):
        """
        Wrapper to execute queries with error handling.
        """
        try:
            result = await query_func()
            return result
        except PyMongoError as e:
            logger.error(f"MongoDB query failed: {str(e)}")
            raise RuntimeError("Database query failed.") from e

mongo = MongoDB(uri=settings.MONGO_URI, db_name=settings.DB_NAME)
