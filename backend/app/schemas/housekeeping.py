from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class HousekeepingLogCreate(BaseModel):
    room_id: int
    cleaning_type: str  # 'checkout', 'stayover', 'deep_clean'
    start_time: datetime
    notes: Optional[str] = None

class HousekeepingLogUpdate(BaseModel):
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class HousekeepingLogResponse(HousekeepingLogCreate):
    id: int
    staff_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class InventoryItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: str
    quantity: int = Field(default=0, ge=0)
    reorder_level: int = Field(..., ge=0)
    unit_price: Optional[float] = None

class InventoryItemResponse(InventoryItemCreate):
    id: int
    last_restocked: datetime
    
    class Config:
        from_attributes = True
