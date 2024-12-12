from app.database import get_collection
from app.redis_client import get_redis_client
from app.config import settings
from app.services.websocket_service import WebSocketService
from app.services.seat_management_service import SeatManagementService
from fastapi import HTTPException
from datetime import datetime, timezone
import asyncio
import logging
logger = logging.getLogger("WaitlistService")


class WaitlistService:
    """
    Service layer for handling the waitlist workflow, including adding parties,
    checking readiness, and managing check-ins.
    """

    @staticmethod
    async def add_to_waitlist(name: str, party_size: int, user_id: str):
        """
        Add a new party to the waitlist and trigger a readiness check.
        """
        try:
            collection = await get_collection("waitlist")
            new_party = {
                "_id": user_id,
                "name": name,
                "party_size": party_size,
                "status": "waiting",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            await collection.insert_one(new_party)
            logger.info(f"Party added to waitlist: {new_party['name']} ({new_party['party_size']} people)")

            # Trigger readiness check outside of scheduler for immediate feedback alongside the periodic checks.
            await WaitlistService.check_queue_readiness()

            return {"message": "Party added to the waitlist.", "party": new_party}
        except Exception as e:
            logger.error(f"Error adding party to waitlist: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def check_queue_readiness():
        """
        Check the waitlist queue for the next party that can be seated.
        If seats are available, notify the party and mark them as ready.
        """
        redis_client = await get_redis_client()
        lock_acquired = await SeatManagementService.acquire_seats_lock(redis_client)
        if not lock_acquired:
            logger.info("Another process is already handling the readiness check.")
            return
        
        try:
            collection = await get_collection("waitlist")
            redis_client = await get_redis_client()
            available_seats = int(await redis_client.get("available_seats") or 0)
            next_party = await collection.find_one({"status": "waiting"}, sort=[("created_at", 1)])
            if next_party and available_seats >= next_party["party_size"]:
                # Mark the party as ready and notify
                updated_party = await collection.find_one_and_update({"_id": next_party["_id"]},{"$set": {"status": "ready"}},return_document=True)
                await redis_client.decrby("available_seats", next_party["party_size"])
                await WebSocketService.notify_ready_party(next_party["_id"], updated_party)
                logger.info(f"Party {next_party['_id']} notified as ready.")
        except Exception as e:
            logger.error(f"Error during readiness check: {e}")
        finally:
            await SeatManagementService.release_seats_lock(redis_client)

    @staticmethod
    async def check_in_party(user_id: str):
        """
        Check in a party, update seats, and start the service.
        """
        redis_client = await get_redis_client()
        collection = await get_collection("waitlist")
        try:
            
            party = await WaitlistService.fetch_and_validate_party(collection, user_id)
            await WaitlistService.mark_party_checked_in(collection, user_id)
            return {"message": "Party checked in successfully"}
        
        except Exception as e:
            logger.error(f"Error during check-in for party {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            asyncio.create_task(WaitlistService.simulate_service(collection, redis_client, party))
            

    @staticmethod
    async def fetch_and_validate_party(collection, user_id: str):
        """
        Fetch the party from the waitlist and validate check-in readiness.
        """
        party = await collection.find_one({"_id": user_id})
        if not party:
            logger.error(f"Party {user_id} not found.")
            raise HTTPException(status_code=404, detail="Party not found.")
        if party["status"] != "ready":
            logger.error(f"Party {user_id} is not ready for check-in.")
            raise HTTPException(status_code=400, detail="Party is not ready for check-in.")
        logger.info(f"Party {user_id} validated for check-in.")
        return party

    @staticmethod
    async def mark_party_checked_in(collection, party_id: str):
        """
        Update the party's status to 'checked_in' and record the start time.
        """
        await collection.update_one(
            {"_id": party_id},
            {"$set": {"status": "checked_in", "started_at": datetime.now(timezone.utc).isoformat()}},
        )
        logger.info(f"Party {party_id} marked as checked in.")

    @staticmethod
    async def simulate_service(collection, redis_client, party: dict):
        """
        Simulate the service process and update the party's status after completion.
        """
        logger.info(f"Simulating service for party {party['_id']} ({party['party_size']} people).")
        try:
            # Simulate service duration
            await asyncio.sleep(settings.SERVICE_TIME_PER_PERSON * party["party_size"])

            # Mark the party as completed
            await collection.update_one({"_id": party["_id"]}, {"$set": {"status": "completed", "completed_at": datetime.now(timezone.utc).isoformat()}})
            logger.info(f"Party {party['_id']} service completed.")

            lock_acquired = await SeatManagementService.acquire_seats_lock(redis_client)
            if not lock_acquired:
                logger.error("Failed to acquire lock during simulate_service for seat update.")
                raise HTTPException(status_code=429, detail="Seats are being updated. Try again shortly.")

            try:
                await SeatManagementService.increment_available_seats(redis_client, party["party_size"])
                logger.info(f"Seats updated after party {party['_id']} service.")
            finally:
                await SeatManagementService.release_seats_lock(redis_client)

        except Exception as e:
            logger.error(f"Error during simulate_service for party {party['_id']}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

