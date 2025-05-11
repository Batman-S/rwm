import pytest
from unittest.mock import AsyncMock, patch, ANY
from datetime import datetime, timezone
from app.services.waitlist_service import WaitlistService


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_add_to_waitlist(mock_db, patch_dependencies):
    user_id_1 = "test_user_1"
    name_1 = "Test Party 1"
    party_size_1 = 4

    with patch(
        "app.services.seat_management_service.SeatManagementService.get_available_seats",
        return_value=2,
    ):

        await WaitlistService.add_to_waitlist(name_1, party_size_1, user_id_1)

        result = await mock_db.find_one({"_id": user_id_1})

        assert result is not None
        assert result["_id"] == user_id_1
        assert result["name"] == name_1
        assert result["party_size"] == party_size_1
        assert result["status"] == "waiting"

    await mock_db.delete_many({"_id": user_id_1})

    user_id_2 = "test_user_2"
    name_2 = "Test Party 2"
    party_size_2 = 4

    await WaitlistService.add_to_waitlist(name_2, party_size_2, user_id_2)

    result = await mock_db.find_one({"_id": user_id_2})
    assert result is not None
    assert result["_id"] == user_id_2
    assert result["name"] == name_2
    assert result["party_size"] == party_size_2
    assert result["status"] == "ready"


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_get_party_status(mock_db):
    user_id = "test_user_1"

    await mock_db.insert_one(
        {
            "_id": user_id,
            "name": "Test Party",
            "party_size": 4,
            "status": "waiting",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )

    result = await WaitlistService.get_party_status(user_id)

    assert result["status"] == "waiting"
    assert result["party"]["_id"] == user_id


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_check_queue_readiness(mock_db, patch_dependencies):
    user_id_1 = "test_user_1"

    await mock_db.insert_one(
        {
            "_id": user_id_1,
            "name": "Test Party 1",
            "party_size": 4,
            "status": "waiting",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )

    with patch(
        "app.services.seat_management_service.SeatManagementService.get_available_seats",
        return_value=2,
    ):
        await WaitlistService.check_queue_readiness()
        notify_party_status = patch_dependencies["notify_party_status"]
        notify_party_status.assert_called_with(user_id_1, ANY, "waiting")
        party = await mock_db.find_one({"_id": user_id_1})
        assert party["status"] == "waiting"

    await mock_db.delete_many({"_id": user_id_1})

    user_id_2 = "test_user_2"

    await mock_db.insert_one(
        {
            "_id": user_id_2,
            "name": "Test Party 2",
            "party_size": 4,
            "status": "waiting",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )

    await WaitlistService.check_queue_readiness()
    notify_party_status = patch_dependencies["notify_party_status"]
    notify_party_status.assert_called_with(user_id_2, ANY, "ready")
    party = await mock_db.find_one({"_id": user_id_2})
    assert party["status"] == "ready"


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_check_in_party(mock_db, patch_dependencies):
    user_id = "test_user_1"

    await mock_db.insert_one(
        {
            "_id": user_id,
            "name": "Test Party",
            "party_size": 4,
            "status": "ready",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )

    with patch(
        "app.services.waitlist_service.WaitlistService.simulate_service",
        new_callable=AsyncMock,
    ) as mock_simulate_service:
        await WaitlistService.check_in_party(user_id)

        party = await mock_db.find_one({"_id": user_id})
        assert party["status"] == "checked_in"
        assert "started_at" in party

        mock_simulate_service.assert_called_once_with(mock_db, ANY, party)
        notify_party_status = patch_dependencies["notify_party_status"]
        notify_party_status.assert_called_with(user_id, ANY, "checked_in")


@pytest.mark.usefixtures("initialize_database")
@pytest.mark.asyncio
async def test_simulate_service(mock_db, patch_dependencies):
    user_id = "test_user_1"

    await mock_db.insert_one(
        {
            "_id": user_id,
            "name": "Test Party",
            "party_size": 4,
            "status": "checked_in",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
    )

    redis_client = patch_dependencies["redis_client"]
    increment_seats = patch_dependencies["increment_seats"]

    party = await mock_db.find_one({"_id": user_id})
    await WaitlistService.simulate_service(mock_db, redis_client, party)
    updated_party = await mock_db.find_one({"_id": user_id})

    assert updated_party["status"] == "completed"
    assert "completed_at" in updated_party

    increment_seats.assert_called_once_with(redis_client, party["party_size"])
