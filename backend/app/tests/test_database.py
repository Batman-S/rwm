import pytest
import pytest_asyncio
from mongomock_motor import AsyncMongoMockClient
from app.database import MongoDBManager


@pytest_asyncio.fixture() 
async def mock_db_manager():
    manager = MongoDBManager(uri="mongodb://mockuri", db_name="mockdb")
    manager._client = AsyncMongoMockClient() 
    manager._db = manager._client["mockdb"]
    try:
        yield manager 
    finally:
        await manager.close()


@pytest.mark.asyncio
async def test_connect(mock_db_manager):
    assert mock_db_manager._client is not None 
    assert mock_db_manager._db.name == "mockdb"


@pytest.mark.asyncio
async def test_close(mock_db_manager):
    assert mock_db_manager._client is not None
    assert mock_db_manager._db is not None

    await mock_db_manager.close()
   
    assert mock_db_manager._client is None
    assert mock_db_manager._db is None

@pytest.mark.asyncio
async def test_get_collection(mock_db_manager):
    collection_name = "test_collection"
    collection = mock_db_manager.get_collection(collection_name)

    await collection.insert_one({"key": "value"})

    document = await collection.find_one({"key": "value"})
    assert document is not None
    assert document["key"] == "value"


@pytest.mark.asyncio
async def test_get_collection_uninitialized():
    """
    Test if get_collection raises an error when the database is not initialized.
    """
    manager = MongoDBManager(uri="mongodb://mockuri", db_name="mockdb")
    manager._client = None 

    with pytest.raises(RuntimeError, match="Database is not initialized"):
        manager.get_collection("test_collection")
