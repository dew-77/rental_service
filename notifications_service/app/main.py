from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker, Session
from . import models, database, rabbitmq, schemas, dependencies, crud

# Create the database engine and session maker
engine = database.engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the app
app = FastAPI()

# Initialize the database
models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def start_rabbitmq_consumer():
    import threading

    def run_consumer():
        rabbitmq.consume_messages("booking_requests", SessionLocal)

    thread = threading.Thread(target=run_consumer, daemon=True)
    thread.start()


@app.get("/")
def read_root():
    return {"message": "Notifications Service is Running"}


@app.get("/notifications/", response_model=list[schemas.Notification])
def get_notifications(
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(dependencies.get_current_user),
):
    return crud.get_notifications_for_user(db, current_user)