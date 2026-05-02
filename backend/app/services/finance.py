from sqlalchemy.orm import Session
from models.finance import Invoice, Payment, Expense
from models.reservation import Reservation
from schemas.finance import InvoiceCreate, PaymentCreate, ExpenseCreate
from decimal import Decimal
from datetime import datetime, timedelta
import uuid

class FinanceService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_invoice(self, invoice_data: InvoiceCreate) -> Invoice:
        """Fatura oluştur"""
        reservation = self.db.query(Reservation).filter(
            Reservation.id == invoice_data.reservation_id
        ).first()
        
        if not reservation:
            raise ValueError("Reservation not found")
        
        # Vergi hesapla (örneğin %18 KDV)
        subtotal = invoice_data.subtotal
        tax = invoice_data.tax_amount or (subtotal * Decimal("0.18"))
        total = subtotal + tax
        
        invoice = Invoice(
            invoice_number=self._generate_invoice_number(),
            reservation_id=invoice_data.reservation_id,
            subtotal=subtotal,
            tax_amount=tax,
            total_amount=total,
            due_date=datetime.utcnow().date() + timedelta(days=30),
            notes=invoice_data.notes
        )
        
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice
    
    def process_payment(self, payment_data: PaymentCreate) -> Payment:
        """Ödemeyi işle"""
        invoice = self.db.query(Invoice).filter(
            Invoice.id == payment_data.invoice_id
        ).first()
        
        if not invoice:
            raise ValueError("Invoice not found")
        
        # Toplam ödenen miktarı kontrol et
        total_paid = self.db.query(func.sum(Payment.amount)).filter(
            Payment.invoice_id == payment_data.invoice_id
        ).scalar() or Decimal("0")
        
        if total_paid + payment_data.amount > invoice.total_amount:
            raise ValueError("Payment exceeds invoice total")
        
        payment = Payment(
            invoice_id=payment_data.invoice_id,
            payment_method=payment_data.payment_method,
            amount=payment_data.amount,
            reference_number=payment_data.reference_number,
            notes=payment_data.notes
        )
        
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
    
    def record_expense(self, expense_data: ExpenseCreate, user_id: int) -> Expense:
        """Gider kaydı oluştur"""
        expense = Expense(
            category=expense_data.category,
            description=expense_data.description,
            amount=expense_data.amount,
            supplier_name=expense_data.supplier_name,
            invoice_date=expense_data.invoice_date,
            created_by=user_id
        )
        
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense
    
    def get_revenue_report(self, start_date, end_date):
        """Gelir raporunu al"""
        invoices = self.db.query(Invoice).filter(
            Invoice.issued_at >= start_date,
            Invoice.issued_at <= end_date
        ).all()
        
        total_revenue = sum(float(inv.total_amount) for inv in invoices)
        total_paid = sum(
            float(payment.amount) 
            for inv in invoices 
            for payment in inv.payments
        )
        
        return {
            "total_revenue": total_revenue,
            "total_paid": total_paid,
            "pending": total_revenue - total_paid,
            "invoice_count": len(invoices)
        }
    
    def _generate_invoice_number(self) -> str:
        """Benzersiz fatura nu
