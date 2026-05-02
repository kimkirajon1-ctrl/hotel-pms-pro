from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Guest(Base):
    __tablename__ = "guests"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    id_type = Column(String(50))  # 'passport', 'id_card', 'license'
    id_number = Column(String(50), unique=True, index=True)
    loyalty_points = Column(Integer, default=0)
    total_spent = Column(Numeric(12, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    reservations = relationship("Reservation", back_populates="guest")
