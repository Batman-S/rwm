from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import mongo
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s | %(message)s",
)
logger = logging.getLogger("WaitlistApp")

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Lifespan context manager for managing startup and shutdown events.
    """
    try:
        logger.info("Starting Waitlist Manager API...")
        await mongo.connect()
        yield
    finally:
        logger.info("Shutting down Waitlist Manager API...")
        await mongo.close()

app = FastAPI(
    title="Waitlist Manager API",
    description="API for managing restaurant waitlists",
    version="1.0.0",
    lifespan=app_lifespan,
)
