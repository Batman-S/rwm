from fastapi import APIRouter
from app.routes.waitlist import router as waitlist_router

api_router = APIRouter()

api_router.include_router(waitlist_router, tags=["waitlist"], prefix="/waitlist")
