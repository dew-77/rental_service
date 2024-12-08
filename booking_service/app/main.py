import asyncio
import signal
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from . import schemas, crud, dependencies, models, database, rabbitmq

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/rental_objects/", response_model=list[schemas.RentalObject])
def read_rental_objects(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: dict = Depends(dependencies.get_current_user)):
    return crud.get_rental_objects(db, skip=skip, limit=limit)


@app.post("/rental_objects/", response_model=schemas.RentalObject)
def create_rental_object(
    rental: schemas.RentalObjectCreate, 
    db: Session = Depends(database.get_db), 
    current_user: dict = Depends(dependencies.get_current_user)
):
    user_id = current_user["user_id"]
    print(f"USER ID RECEIVED IN CREATE RENTAL {user_id}")

    return crud.create_rental_object(db, rental, user_id)


# @app.post("/bookings/", response_model=schemas.Booking)
# def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db), current_user: dict = Depends(dependencies.get_current_user)):
#     return crud.create_booking(db, booking)


@app.post("/request_booking/", response_model=schemas.Request)
def request_booking(
    request_data: schemas.RequestCreate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(dependencies.get_current_user)
):
    # Step 1: Create a "Request" object
    request = models.Request(
        rental_object_id=request_data.rental_object_id,
        user_id=current_user["user_id"],
        status="open"
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    
    rental_object = db.query(models.RentalObject).filter(models.RentalObject.id == request.rental_object_id).first()

    # Step 2: Send a message to the notification service
    message = {
        "renter": request.user_id,
        "landlord": rental_object.user_id,
        "rental_object_id": request.rental_object_id,
        "status": request.status,
        "request_id": request.id,
        "message": f"New booking request {request.id} for object {request.rental_object_id}",
        "for": "landlord"
    }
    rabbitmq.publish_message("booking_requests", message)

    return request


@app.post("/update_request_status/{request_id}", response_model=schemas.Request)
def update_request_status(
    request_id: int,
    request_data: schemas.RequestStatusUpdate,  # Accept the status update request as a schema
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(dependencies.get_current_user)
):
    # Step 1: Get the request object
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Step 2: Ensure that the current user is the landlord
    rental_object = db.query(models.RentalObject).filter(models.RentalObject.id == request.rental_object_id).first()
    if not rental_object or rental_object.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="You are not the landlord of this rental object")

    # Step 3: Validate the status and update the request status
    if request_data.status not in ["accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'accepted' or 'rejected'")

    request.status = request_data.status
    db.commit()
    db.refresh(request)

    # Step 4: Send a notification to the renter and landlord
    message = {
        "renter": request.user_id,
        "landlord": rental_object.user_id,
        "rental_object_id": request.rental_object_id,
        "status": request.status,
        "request_id": request.id,
        "message": f"New status for your request to object {request.rental_object_id}: {request.status}.",
        "for": "renter"
    }
    rabbitmq.publish_message("booking_requests", message)

    return request


def process_user_data(message: dict, db: Session):
    print("Received user data:", message)
    user_id = message["user_id"]
    username = message["username"]
    email = message["email"]
    db_user = crud.create_user(db, user_id, username, email)
    print(f"User {username} saved to the booking system with ID {db_user.id}")


async def start_message_consumer():
    # Start the message consumer in the background
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, rabbitmq.consume_messages, 'user_registration', process_user_data)


@app.on_event("startup")
async def startup():
    # Start the message consumer when the app starts
    app.state.consumer_task = asyncio.create_task(start_message_consumer())
    ...


@app.on_event("shutdown")
async def shutdown():
    # Cleanly shutdown the message consumer task on app shutdown
    if app.state.consumer_task:
        app.state.consumer_task.cancel()  # Cancel the consumer task
        try:
            await app.state.consumer_task  # Wait for the task to be fully canceled
        except asyncio.CancelledError:
            pass


@app.get("/")
def read_root():
    return {"message": "Booking Service is Running"}

