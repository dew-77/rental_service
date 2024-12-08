from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RentalObject(Base):
    __tablename__ = "rental_objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price_per_day = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    user_id = Column(Integer, nullable=False)


    bookings = relationship("Booking", back_populates="rental_object")
    requests = relationship("Request", back_populates="rental_object")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    rental_object_id = Column(Integer, ForeignKey("rental_objects.id"), nullable=False)
    user_id = Column(Integer, nullable=False)  # From auth_service
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)

    rental_object = relationship("RentalObject", back_populates="bookings")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)  # user_id from auth_service
    username = Column(String, index=True)
    email = Column(String, index=True)

    # Add any other fields that might be necessary in the future

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}, email={self.email}>"
    

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    rental_object_id = Column(Integer, ForeignKey("rental_objects.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(String, default="open", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    rental_object = relationship("RentalObject", back_populates="requests")