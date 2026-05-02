from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class HousekeepingLog(Base):
    __tablename__ = "housekeeping_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    staff_id = Column(Integer, nullable=False)  # User ID
    cleaning_type = Column(String(50), nullable=False)  # 'checkout', 'stayover', 'deep_clean'
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String(50), default="in_progress")  # 'completed', 'pending'
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False, index=True)  # 'linens', 'toiletries', 'cleaning'
    quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, nullable=False)
    unit_price = Column(Integer)
    last_restocked = Column(DateTime, default=datetime.utcnow)
    supplier_id = Column(Integer)
