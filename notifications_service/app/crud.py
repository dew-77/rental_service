from sqlalchemy.orm import Session
from . import models, schemas


def create_notification(db: Session, message: dict):
    notification = models.Notification(
        user_id=message[message["for"]],
        message=message["message"]
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    print('Created new notification.')
    return notification

def get_notifications_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """
    Retrieve notifications for a specific user from the database.
    :param db: Database session
    :param user_id: ID of the user
    :param skip: Number of records to skip (for pagination)
    :param limit: Maximum number of records to return (for pagination)
    :return: List of notifications
    """
    return db.query(models.Notification) \
        .filter(models.Notification.user_id == user_id) \
        .offset(skip) \
        .limit(limit) \
        .all()