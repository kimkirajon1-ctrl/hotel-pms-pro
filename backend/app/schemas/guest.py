from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class GuestCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    id_type: Optional[str] = None  # 'passport', 'id_card'
    id_number: Optional[str] = None

class GuestUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    loyalty_points: Optional[int] = None

class GuestResponse(GuestCreate):
    id: int
    loyalty_points: int
    total_spent: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
