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
    async def get_party_status(user_id: str):
        """
        Retrieve the current status of a party in the waitlist by user_id.
        """
        try:
            collection = await get_collection("waitlist")
            party = await collection.find_one({"_id": user_id})
            if not party:
                return {"status": "na"}

            return {"status": party["status"], "party": party}

        except Exception as e:
            logger.error(f"Error retrieving party status for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

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
            available_seats = await SeatManagementService.get_available_seats(redis_client)
            next_party = await collection.find_one({"status": "waiting"}, sort=[("created_at", 1)])
            
            if next_party and available_seats < next_party["party_size"]:
                await WebSocketService.notify_party_status(next_party["_id"], next_party, "waiting")
            
            if next_party and available_seats >= next_party["party_size"]:
                # Mark the party as ready and notify
                updated_party = await collection.find_one_and_update({"_id": next_party["_id"]},{"$set": {"status": "ready"}},return_document=True)
                await SeatManagementService.decrement_available_seats(redis_client, next_party["party_size"])
                await WebSocketService.notify_party_status(next_party["_id"], updated_party, "ready")
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
            updated_party = await collection.find_one_and_update(
            {"_id": user_id},
            {"$set": {"status": "checked_in", "started_at": datetime.now(timezone.utc).isoformat()}}, return_document=True)
            await WebSocketService.notify_party_status(user_id,updated_party,"checked_in")
            return {"message": "Party checked in successfully"}
        
        except Exception as e:
            logger.error(f"Error during check-in for party {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            asyncio.create_task(WaitlistService.simulate_service(collection, redis_client, updated_party))

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
            updated_party = await collection.find_one_and_update({"_id": party["_id"]}, {"$set": {"status": "completed", "completed_at": datetime.now(timezone.utc).isoformat()}}, return_document=True)
            await WebSocketService.notify_party_status(party["_id"], updated_party, "completed")
            
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

