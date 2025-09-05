from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List
from datetime import datetime
import re

app = FastAPI(
    title="STD24001",
    description="This is a specification of STD24001",
    version="1.0.0"
)


bookings_storage: List[dict] = []


class Customer(BaseModel):
    customerName: str = Field(..., description="Nom du client")
    phoneNumber: str = Field(..., description="Numéro de téléphone du client")
    email: EmailStr = Field(..., description="Adresse email du client")

class Room(BaseModel):
    roomNumber: int = Field(..., ge=1, le=9, description="Numéro de chambre (entre 1 et 9 uniquement)")
    roomDescription: str = Field(..., description="Description de la chambre")

class BookingRequest(BaseModel):
    customerName: str = Field(..., description="Nom du client")
    phoneNumber: str = Field(..., description="Numéro de téléphone du client")
    email: EmailStr = Field(..., description="Adresse email du client")
    roomNumber: int = Field(..., ge=1, le=9, description="Numéro de chambre (entre 1 et 9 uniquement)")
    roomDescription: str = Field(..., description="Description de la chambre")
    reservationDate: str = Field(..., description="Date de la réservation au format DD/MM/YYYY")
    
    @validator('reservationDate')
    def validate_date_format(cls, v):
        try:
         
            datetime.strptime(v, '%d/%m/%Y')
            return v
        except ValueError:
            raise ValueError('La date doit être au format DD/MM/YYYY')

class Booking(BookingRequest):
    pass

class ErrorResponse(BaseModel):
    message: str = Field(..., description="Message d'erreur")
    code: int = Field(..., description="Code d'erreur")

def is_room_available(room_number: int, reservation_date: str) -> bool:
    """Vérifie si une chambre est disponible à une date donnée"""
    for booking in bookings_storage:
        if booking['roomNumber'] == room_number and booking['reservationDate'] == reservation_date:
            return False
    return True

@app.get("/booking", response_model=List[Booking])
async def get_bookings():
    """Récupérer la liste des réservations sauvegardée dans la mémoire vive"""
    return bookings_storage

@app.post("/booking", response_model=List[Booking])
async def create_booking(booking_request: BookingRequest):
    """Créer une nouvelle réservation"""

    if not is_room_available(booking_request.roomNumber, booking_request.reservationDate):
        raise HTTPException(
            status_code=400,
            detail={
                "message": "La chambre n'est plus disponible pour cette date",
                "code": 400
            }
        )
    
   
    new_booking = booking_request.dict()
    bookings_storage.append(new_booking)
    
  
    return bookings_storage

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)