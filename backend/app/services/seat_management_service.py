from redis.asyncio import Redis
from fastapi import HTTPException
import logging

logger = logging.getLogger("SeatManagement")

class SeatManagementService:
    """
    Service layer for managing seat availability and concurrency locks.
    """

    @staticmethod
    async def acquire_seats_lock(redis_client: Redis) -> bool:
        """
        Acquire a Redis lock for updating seats.
        """
        try:
            lock_acquired = await redis_client.set(
                "seats_lock", "locked", ex=5, nx=True
            )
            if lock_acquired:
                logger.info("Seats lock acquired.")
            else:
                logger.warning("Failed to acquire seats lock.")
            return lock_acquired
        except Exception as e:
            logger.error(f"Error acquiring seats lock: {e}")
            raise HTTPException(status_code=500, detail="Failed to acquire lock.")

    @staticmethod
    async def release_seats_lock(redis_client: Redis):
        """
        Release the Redis lock for seat management.
        """
        try:
            await redis_client.delete("seats_lock")
            logger.info("Seats lock released.")
        except Exception as e:
            logger.error(f"Error releasing seats lock: {e}")
            raise HTTPException(status_code=500, detail="Failed to release lock.")

    @staticmethod
    async def decrement_available_seats(redis_client: Redis, party_size: int):
        """
        Decrement available seats by the party size.
        """
        try:
            available_seats = int(await redis_client.get("available_seats") or 0)
            logger.info(f"Available seats before decrement: {available_seats}")
            if available_seats < party_size:
                logger.warning(
                    f"Not enough available seats. Requested: {party_size}, Available: {available_seats}"
                )
                raise HTTPException(status_code=400, detail="Not enough available seats.")

            await redis_client.decrby("available_seats", party_size)
            logger.info(f"Decremented available seats by {party_size}.")
        except Exception as e:
            logger.error(f"Error decrementing available seats: {e}")
            raise HTTPException(status_code=500, detail="Failed to update available seats.")

    @staticmethod
    async def increment_available_seats(redis_client: Redis, party_size: int):
        """
        Increment available seats by the party size.
        """
        try:
            await redis_client.incrby("available_seats", party_size)
            logger.info(f"Incremented available seats by {party_size}.")
        except Exception as e:
            logger.error(f"Error incrementing available seats: {e}")
            raise HTTPException(status_code=500, detail="Failed to update available seats.")

    @staticmethod
    async def get_available_seats(redis_client: Redis) -> int:
        """
        Retrieve the current number of available seats from Redis.
        """
        try:
            available_seats = int(await redis_client.get("available_seats") or 0)
            logger.info(f"Retrieved available seats: {available_seats}")
            return available_seats
        except Exception as e:
            logger.error(f"Error retrieving available seats: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve available seats.")
