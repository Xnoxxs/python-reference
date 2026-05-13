
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    authentication_id: str
    name: str
    email: str
    password: Optional[str]
    created: datetime
    photo: str
    push_notifications_permission: bool
    devices_tokens: List[str]

    # Derived
    # This is not a db field of user, it is computed
    bookings_count: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
