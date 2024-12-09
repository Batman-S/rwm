from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WaitlistCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,)
    party_size: int = Field(..., gt=0, le=10)

class WaitlistResponse(BaseModel):
    id: Optional[str] = Field(None)
    name: str = Field(...)
    party_size: int = Field(...)
    status: str = Field(...) 
    created_at: datetime = Field(...)

    class Config:
        populate_by_name = True
       

class WaitlistUpdate(BaseModel):
    status: Optional[str] = Field(None)

 