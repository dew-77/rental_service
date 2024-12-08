from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    message: str
    is_read: bool = False

class Notification(NotificationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
