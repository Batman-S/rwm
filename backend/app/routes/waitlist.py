from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson import ObjectId
from app.database import get_collection
from app.schemas import WaitlistCreate, WaitlistResponse
from app.models import waitlist_model
import logging

router = APIRouter()
logger = logging.getLogger("WaitlistRoutes")

@router.post("/", response_model=WaitlistResponse, summary="Add to Waitlist")
async def add_to_waitlist(
    party: WaitlistCreate,
    collection: Collection = Depends(lambda: get_collection('waitlist')),
):
    try:
        
        new_party = waitlist_model(name=party.name, party_size=party.party_size)
        result = await collection.insert_one(new_party)

        new_party["_id"] = str(result.inserted_id)
        logger.info(f"Party added to waitlist: {new_party['name']} ({new_party['party_size']})")
        return new_party
    except Exception as e:
        logger.error(f"Failed to add party to waitlist: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add party to waitlist.")

@router.get("/{party_id}", response_model=WaitlistResponse, summary="Get Waitlist Entry")
async def get_waitlist_entry(
    party_id: str,
    collection: Collection = Depends(lambda: get_collection('waitlist')),
):
    try:
        entry = await collection.find_one({"_id": ObjectId(party_id)})
        if not entry:
            raise HTTPException(status_code=404, detail="Waitlist entry not found.")
        
        entry["_id"] = str(entry["_id"])
        return entry
    except Exception as e:
        logger.error(f"Failed to retrieve waitlist entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve waitlist entry.")

@router.delete("/{party_id}", summary="Remove Waitlist Entry")
async def remove_waitlist_entry(
    party_id: str,
    collection: Collection = Depends(lambda: get_collection('waitlist')),
):
    try:
        result = await collection.delete_one({"_id": ObjectId(party_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Waitlist entry not found.")

        logger.info(f"Waitlist entry with ID {party_id} removed.")
        return {"message": "Waitlist entry removed successfully."}
    except Exception as e:
        logger.error(f"Failed to remove waitlist entry: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to remove waitlist entry.")
