from fastapi import FastAPI
from socketio import AsyncServer, ASGIApp
from app.socket_io import setup_socketio_events
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api_router
from app.database import db_manager
from app.redis_client import get_redis_client
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s | %(message)s",
)
logger = logging.getLogger("WaitlistApp")

scheduler = AsyncIOScheduler()
def setup_scheduler():
    """
    Setup the scheduler for periodic tasks.
    """
    from app.services.waitlist_service import WaitlistService

    scheduler.add_job(
        WaitlistService.check_queue_readiness,
        trigger="interval",
        seconds=5,
        id="check_queue_readiness",
    )
    scheduler.start()
    logger.info("Scheduler started with job: check_queue_readiness")


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Manage startup and shutdown events for the app.
    """
    try:
        logger.info("Starting Waitlist Manager API...")
        await db_manager.connect()
        await setup_socketio_events(sio)

        # Initialize seats in Redis on app start. TODO: Save available seats to disk
        redis_client = await get_redis_client()
        if await redis_client.get("available_seats") is None:
            await redis_client.set("available_seats", 10)
            logger.info("Initialized available_seats to 10 in Redis")
            
        setup_scheduler()
        yield
    finally:
        logger.info("Shutting down Waitlist Manager API...")
        scheduler.shutdown()  
        await db_manager.close() 

app = FastAPI(
    title="Waitlist Manager API",
    description="API for managing restaurant waitlists with real-time updates",
    version="1.0.0",
    lifespan=app_lifespan,
)

# Mount socket server
sio = AsyncServer(async_mode="asgi", cors_allowed_origins="http://localhost:5173")
app.mount("/ws", ASGIApp(sio))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
