import pytest
from app.services.seat_management_service import SeatManagementService
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_acquire_seats_lock():
    with patch(
        "app.redis_client.get_redis_client", new_callable=AsyncMock
    ) as mock_get_redis_client:
        mock_redis_client = mock_get_redis_client.return_value
        await SeatManagementService.acquire_seats_lock(mock_redis_client)

        mock_redis_client.set.assert_called_once_with(
            "seats_lock", "locked", ex=5, nx=True
        )


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_release_seats_lock():
    with patch(
        "app.redis_client.get_redis_client", new_callable=AsyncMock
    ) as mock_get_redis_client:
        mock_redis_client = mock_get_redis_client.return_value
        await SeatManagementService.release_seats_lock(mock_redis_client)

        mock_redis_client.delete.assert_called_once_with("seats_lock")


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_get_available_seats():
    with patch(
        "app.redis_client.get_redis_client", new_callable=AsyncMock
    ) as mock_get_redis_client:
        mock_redis_client = mock_get_redis_client.return_value
        mock_redis_client.get.return_value = "10"

        available_seats = await SeatManagementService.get_available_seats(
            mock_redis_client
        )

        mock_redis_client.get.assert_called_once_with("available_seats")
        assert available_seats == 10


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_increment_available_seats():
    with patch(
        "app.redis_client.get_redis_client", new_callable=AsyncMock
    ) as mock_get_redis_client:
        mock_redis_client = mock_get_redis_client.return_value

        party_size = 4
        await SeatManagementService.increment_available_seats(
            mock_redis_client, party_size
        )

        mock_redis_client.incrby.assert_called_once_with("available_seats", party_size)


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_decrement_available_seats():
    with patch(
        "app.redis_client.get_redis_client", new_callable=AsyncMock
    ) as mock_get_redis_client:
        mock_redis_client = mock_get_redis_client.return_value
        mock_redis_client.get.return_value = 10

        party_size = 4
        await SeatManagementService.decrement_available_seats(
            mock_redis_client, party_size
        )

        mock_redis_client.decrby.assert_called_once_with("available_seats", party_size)


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_decrement_available_seats_fail_not_enough():
    with patch(
        "app.redis_client.get_redis_client", new_callable=AsyncMock
    ) as mock_get_redis_client:
        mock_redis_client = mock_get_redis_client.return_value
        mock_redis_client.get.return_value = 2  # Available seats: 2

        with pytest.raises(HTTPException):
            await SeatManagementService.decrement_available_seats(mock_redis_client, 4)

        mock_redis_client.get.assert_called_once_with("available_seats")
