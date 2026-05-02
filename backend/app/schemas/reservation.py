from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class ReservationCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in: date
    check_out: date
    notes: Optional[str] = None

class ReservationUpdate(BaseModel):
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    notes: Optional[str] = None

class ReservationResponse(ReservationCreate):
    id: int
    reservation_number: str
    status: str
    total_amount: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
