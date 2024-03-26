from datetime import date, datetime
from pydantic import BaseModel


class Reservation(BaseModel):
    id: str
    client_id: str
    apartment_id: str
    start_date: str
    end_date: str
    status: str

class UpdateReservationModel(BaseModel):
    client_id: str
    apartment_id: str
    start_date: str
    end_date: str
    status: str