from sqlalchemy.orm import Session
from . import models, schemas


def create_user(db: Session, user_id: int, username: str, email: str):
    db_user = models.User(user_id=user_id, username=username, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_rental_objects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.RentalObject).offset(skip).limit(limit).all()


def create_rental_object(db: Session, rental: schemas.RentalObjectCreate, user_id: int):
    db_rental_object = models.RentalObject(
        name=rental.name,
        description=rental.description,
        price_per_day=rental.price_per_day,
        is_available=rental.is_available,
        user_id=user_id
    )
    db.add(db_rental_object)
    db.commit()
    db.refresh(db_rental_object)
    return db_rental_object



def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
