from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from typing import Optional


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
        except Exception as e:
            raise RuntimeError("Failed to connect to DB") from e

    async def close(self) -> None:
        if self._client:
            self._client.close()


mongo = MongoDB(uri=settings.MONGO_URI, db_name=settings.DB_NAME)
