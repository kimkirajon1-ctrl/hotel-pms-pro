from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RoomCreate(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=10)
    room_type: str
    floor: int = Field(..., ge=1)
    capacity: int = Field(default=2, ge=1)
    price_per_night: float = Field(..., gt=0)
    description: Optional[str] = None

class RoomResponse(RoomCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
