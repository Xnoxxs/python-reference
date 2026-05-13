from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING, Optional
from datetime import datetime

from train.pydantic.schemas.user import UserSchema

if TYPE_CHECKING:
    from train.pydantic.schemas.booking import BookingSchema


class ReviewSchema(BaseModel):
    id: int
    booking_id: int
    score: float
    comment: Optional[str]
    date: datetime

    # Relationships
    user: UserSchema
    booking: Optional[BookingSchema] = None

    model_config = ConfigDict(from_attributes=True)
