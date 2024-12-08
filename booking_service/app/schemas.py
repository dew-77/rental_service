from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RentalObjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_day: float
    is_available: Optional[bool] = True


class RentalObjectCreate(RentalObjectBase):
    pass


class RentalObject(RentalObjectBase):
    id: int

    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    rental_object_id: int
    user_id: int
    start_date: str
    end_date: str


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True


class RequestBase(BaseModel):
    rental_object_id: int
    status: Optional[str] = "open"


class RequestCreate(RequestBase):
    pass


class Request(RequestBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RequestStatusUpdate(BaseModel):
    status: str  # "accepted" or "rejected"