from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class InvoiceCreate(BaseModel):
    reservation_id: int
    subtotal: Decimal = Field(..., gt=0)
    tax_amount: Optional[Decimal] = None
    notes: Optional[str] = None

class InvoiceResponse(InvoiceCreate):
    id: int
    invoice_number: str
    total_amount: Decimal
    issued_at: datetime
    due_date: Optional[date] = None
    
    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    invoice_id: int
    payment_method: str  # 'cash', 'credit_card', 'bank_transfer', 'corporate'
    amount: Decimal = Field(..., gt=0)
    reference_number: Optional[str] = None
    notes: Optional[str] = None

class PaymentResponse(PaymentCreate):
    id: int
    payment_date: datetime
    
    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    category: str
    description: str
    amount: Decimal = Field(..., gt=0)
    supplier_name: Optional[str] = None
    invoice_date: date

class ExpenseResponse(ExpenseCreate):
    id: int
    paid_at: Optional[datetime] = None
    created_by: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
