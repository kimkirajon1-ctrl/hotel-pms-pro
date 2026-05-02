from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime
from schemas.room import RoomResponse
from schemas.reservation import ReservationCreate, ReservationResponse
from services.reservation import ReservationService
from core.security import get_current_user
from db.database import get_db

router = APIRouter(prefix="/api/v1/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationResponse)
async def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Yeni bir rezervasyon oluştur"""
    service = ReservationService(db)
    
    # Oda müsaitliğini kontrol et
    if not service.is_room_available(
        reservation.room_id,
        reservation.check_in,
        reservation.check_out
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room not available for selected dates"
        )
    
    new_reservation = service.create(reservation, current_user.id)
    return new_reservation

@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Rezervasyon detaylarını getir"""
    service = ReservationService(db)
    reservation = service.get_by_id(reservation_id)
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    return reservation

@router.post("/{reservation_id}/check-in")
async def check_in(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Misafiri kaydet (Check-in)"""
    service = ReservationService(db)
    reservation = service.check_in(reservation_id)
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    return {"message": "Check-in successful", "reservation_id": reservation_id}
