from sqlalchemy import Column, Integer, String, Enum, Numeric, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class RoomStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    DIRTY = "dirty"
    MAINTENANCE = "maintenance"
    BLOCKED = "blocked"

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(10), unique=True, nullable=False)
    room_type = Column(String(50), nullable=False)  # 'single', 'double', 'suite'
    floor = Column(Integer, nullable=False)
    capacity = Column(Integer, default=2)
    status = Column(Enum(RoomStatus), default=RoomStatus.AVAILABLE)
    price_per_night = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
