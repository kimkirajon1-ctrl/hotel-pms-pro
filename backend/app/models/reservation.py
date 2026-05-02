from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from db.database import Base

class ReservationStatus(str, enum.Enum):
    PENDING = "pending"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    reservation_number = Column(String(20), unique=True, nullable=False, index=True)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in = Column(Date, nullable=False, index=True)
    check_out = Column(Date, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)
    total_amount = Column(Numeric(12, 2), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    guest = relationship("Guest", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")
    invoices = relationship("Invoice", back_populates="reservation")
