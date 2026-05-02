from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.room import Room, RoomStatus
from models.reservation import Reservation, ReservationStatus
from models.guest import Guest
from schemas.reservation import ReservationCreate
from datetime import date

class ReservationService:
    def __init__(self, db: Session):
        self.db = db
    
    def is_room_available(self, room_id: int, check_in: date, check_out: date) -> bool:
        """Belirli tarihler arasında oda müsaitliğini kontrol et"""
        conflicting = self.db.query(Reservation).filter(
            Reservation.room_id == room_id,
            Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CHECKED_IN]),
            and_(
                Reservation.check_in < check_out,
                Reservation.check_out > check_in
            )
        ).first()
        
        return conflicting is None
    
    def create(self, reservation: ReservationCreate, user_id: int):
        """Yeni rezervasyon oluştur"""
        # Fiyat hesapla
        num_nights = (reservation.check_out - reservation.check_in).days
        room = self.db.query(Room).filter(Room.id == reservation.room_id).first()
        total_amount = float(room.price_per_night) * num_nights
        
        new_reservation = Reservation(
            reservation_number=self._generate_reservation_number(),
            guest_id=reservation.guest_id,
            room_id=reservation.room_id,
            check_in=reservation.check_in,
            check_out=reservation.check_out,
            total_amount=total_amount,
            status=ReservationStatus.PENDING,
            notes=reservation.notes
        )
        
        self.db.add(new_reservation)
        self.db.commit()
        self.db.refresh(new_reservation)
        return new_reservation
    
    def check_in(self, reservation_id: int):
        """Misafiri kaydet"""
        reservation = self.db.query(Reservation).filter(
            Reservation.id == reservation_id
        ).first()
        
        if not reservation:
            return None
        
        reservation.status = ReservationStatus.CHECKED_IN
        room = self.db.query(Room).filter(Room.id == reservation.room_id).first()
        room.status = RoomStatus.OCCUPIED
        
        self.db.commit()
        return reservation
    
    def _generate_reservation_number(self) -> str:
        """Benzersiz rezervasyon numarası oluştur"""
        from datetime import datetime
        import uuid
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"RES-{timestamp}-{unique_id}"
