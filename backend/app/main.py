from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import mongo

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Lifespan context manager for managing startup and shutdown events.
    """
    try:
        await mongo.connect()
        yield
    finally:
        await mongo.close()

app = FastAPI(
    title="Waitlist Manager API",
    description="API for managing restaurant waitlists",
    version="1.0.0",
    lifespan=app_lifespan,
)

