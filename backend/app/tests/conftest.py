import pytest
import asyncio
from app.database import db_manager
from unittest.mock import AsyncMock, patch
from dotenv import load_dotenv
load_dotenv(".env.test")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def initialize_database():
    await db_manager.connect()
    assert db_manager._db is not None, "Database connection failed in fixture"
    yield db_manager
    await db_manager.close()

@pytest.fixture(scope="function")
async def mock_db():
    db = db_manager._db
    waitlist_collection = db.get_collection("waitlist")
    await waitlist_collection.delete_many({})
    yield waitlist_collection
    await waitlist_collection.delete_many({})

@pytest.fixture
async def patch_dependencies():
    with (patch("app.redis_client.get_redis_client", new_callable=AsyncMock) as mock_get_redis_client,
         patch("app.services.websocket_service.WebSocketService.notify_party_status", new_callable=AsyncMock) as mock_notify_party_status,
         patch("app.services.seat_management_service.SeatManagementService.acquire_seats_lock", return_value=True, new_callable=AsyncMock) as mock_acquire_lock,
         patch("app.services.seat_management_service.SeatManagementService.release_seats_lock", new_callable=AsyncMock) as mock_release_lock,
         patch("app.services.seat_management_service.SeatManagementService.decrement_available_seats", new_callable=AsyncMock) as mock_decrement_seats,
         patch("app.services.seat_management_service.SeatManagementService.increment_available_seats", new_callable=AsyncMock) as mock_increment_seats):
       
        mock_get_available_seats = AsyncMock(return_value=10) 
        patch("app.services.seat_management_service.SeatManagementService.get_available_seats", mock_get_available_seats)
        mock_redis_client = mock_get_redis_client.return_value
        mock_redis_client.get.return_value = 10  # Mock available seats

        yield {
            "redis_client": mock_redis_client,
            "notify_party_status": mock_notify_party_status,
            "acquire_lock": mock_acquire_lock,
            "release_lock": mock_release_lock,
            "increment_seats": mock_increment_seats,
            "decrement_seats": mock_decrement_seats,
            "get_available_seats": mock_get_available_seats,
        }