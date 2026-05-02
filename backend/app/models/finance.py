from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from db.database import Base

class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    CORPORATE = "corporate"

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(20), unique=True, nullable=False, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(12, 2), nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(Date)
    notes = Column(Text)
    
    # İlişkiler
    reservation = relationship("Reservation", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    reference_number = Column(String(100))
    notes = Column(Text)
    
    # İlişkiler
    invoice = relationship("Invoice", back_populates="payments")

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False, index=True)  # 'supplies', 'maintenance', 'utilities'
    description = Column(Text, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    supplier_name = Column(String(100))
    invoice_date = Column(Date, nullable=False)
    paid_at = Column(DateTime)
    created_by = Column(Integer)  # User ID
    created_at = Column(DateTime, default=datetime.utcnow)
