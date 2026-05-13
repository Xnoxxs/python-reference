from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from train.pydantic.schemas.review import UserSchema
from train.pydantic.schemas.review import ReviewSchema


class BookingSchema(BaseModel):
    id: int
    activity_id: int
    user_id: int

    status: str

    schedule_type: str
    slot_id: Optional[int]

    reservation_date: datetime

    people: int
    activity_price: int
    total_price: int

    code: str
    asked_for_rating: bool

    review: Optional[ReviewSchema] = None
    user: Optional[UserSchema]

    model_config = ConfigDict(from_attributes=True)



