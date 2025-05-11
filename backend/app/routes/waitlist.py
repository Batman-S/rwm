from fastapi import APIRouter, Body
from app.services.waitlist_service import WaitlistService

router = APIRouter()


@router.get("/waitlist/{user_id}/status")
async def get_waitlist_status(user_id: str):
    return await WaitlistService.get_party_status(user_id)


@router.post("/waitlist")
async def add_party_to_waitlist(
    name: str = Body(...), party_size: int = Body(...), user_id: str = Body(...)
):
    return await WaitlistService.add_to_waitlist(name, party_size, user_id)


@router.post("/waitlist/{user_id}/check-in")
async def check_in(user_id: str):
    return await WaitlistService.check_in_party(user_id)
