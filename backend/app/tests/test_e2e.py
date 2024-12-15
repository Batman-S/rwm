import pytest
import asyncio
from app.main import app as client_app
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager
from datetime import datetime, timezone
from testcontainers.mongodb import MongoDbContainer
from testcontainers.redis import RedisContainer
from testcontainers.core.container import DockerContainer
import logging
logging.basicConfig(level=logging.INFO)
DockerContainer.DEFAULT_LOG_LEVEL = logging.DEBUG
from app.config import settings

@pytest.fixture(scope="session")
async def setup_containers():
    """
    Spin up MongoDB and Redis containers for the test session.
    """
    with MongoDbContainer() as mongo, RedisContainer() as redis:
        mongo_url = mongo.get_connection_url()
        redis_url = f"redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(6379)}"

        settings.MONGO_URI = mongo_url
        settings.REDIS_URL = redis_url

        from app.database import db_manager
        from app.redis_client import redis_manager
    
        await db_manager.close()
        await redis_manager.close()
        
        db_manager._client = None
        redis_manager._redis = None
        
        db_manager._uri = mongo_url
        redis_manager._redis_url = redis_url
        
        await db_manager.connect()
        await redis_manager.connect() 

        yield
        
      
@pytest.fixture(scope="function")
async def client():
    """
    Provides an async TestClient instance for the test function.
    
    """
    async with LifespanManager(client_app) as manager:
        async with AsyncClient(transport=ASGITransport(app=manager.app), base_url="http://testserver") as client:
            yield client
               
@pytest.mark.usefixtures("setup_containers")     
@pytest.mark.asyncio
async def test_full_waitlist_flow_for_multiple_users(client):
    """
    Test the full flow of adding a party to the waitlist, checking them in, and waiting for completion before checking in the next available parties.
    """
    user_ids = ["user_1", "user_2", "user_3", "user_4"]
    party_sizes = [3, 6, 4, 5]
    service_time = 3
    parties = []
    for i, user_id in enumerate(user_ids):
        payload = {
            "name": f"Test Party {user_id}",
            "party_size": party_sizes[i],
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        parties.append(payload)
        response = await client.post("/api/v1/waitlist", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["party"]["name"] == f"Test Party {user_id}"
        assert data["party"]["party_size"] == party_sizes[i]
        assert data["party"]["status"] == "waiting"

    sorted_parties = sorted(parties, key=lambda x: x['created_at'])
    ready_parties = [(sorted_parties[i]['user_id'], sorted_parties[i]['party_size']) for i in range(2)]
    waiting_parties = [(sorted_parties[i]['user_id'], sorted_parties[i]['party_size']) for i in range(2, len(sorted_parties))]

    async def check_in_parties(parties):
        total_diners = 0

        for user_id, _ in parties:
            response = await client.get(f"/api/v1/waitlist/{user_id}/status")
            assert response.status_code == 200
            status_data = response.json()
            assert status_data["status"] == "ready"

        for user_id, party_size in parties:
            response = await client.post(f"/api/v1/waitlist/{user_id}/check-in")
            assert response.status_code == 200
            status_response = await client.get(f"/api/v1/waitlist/{user_id}/status")
            status_data = status_response.json()
            assert status_data["status"] == "checked_in"
            total_diners += party_size

        await asyncio.sleep(total_diners * service_time)

        for user_id, party_size in parties:
            response = await client.get(f"/api/v1/waitlist/{user_id}/status")
            assert response.status_code == 200
            service_complete_data = response.json()
            assert service_complete_data["status"] == "completed"

    await check_in_parties(ready_parties)
    await check_in_parties(waiting_parties)
