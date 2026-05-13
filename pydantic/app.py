"""Scratch space: validate plain dicts with the ORM-facing Pydantic schemas.

Do not name this file app.py: when run from this directory, Python would load it as
top-level `app` and break `from app.schemas...` imports used by the train schemas.
"""

from datetime import datetime, timezone

from train.pydantic.schemas.booking import BookingSchema
from train.pydantic.schemas.review import ReviewSchema
from train.pydantic.schemas.user import UserSchema

if __name__ == "__main__":
    now = datetime.now(timezone.utc)

    user = UserSchema.model_validate(
        {
            "id": 1,
            "authentication_id": "firebase_users-demo",
            "name": "Demo User",
            "email": "demo@example.com",
            "password": None,
            "created": now,
            "photo": "",
            "push_notifications_permission": True,
            "devices_tokens": [],
            "owner": None,
            "bookings_count": 3,
        }
    )

    booking = BookingSchema.model_validate(
        {
            "id": 10,
            "activity_id": 2,
            "user_id": user.id,
            "status": "success",
            "schedule_type": "slots",
            "slot_id": 99,
            "reservation_date": now,
            "people": 2,
            "activity_price": 1500,
            "total_price": 3000,
            "code": "DEMO-CODE",
            "asked_for_rating": False,
            "review": None,
            "user": user,
        }
    )

    review = ReviewSchema.model_validate(
        {
            "id": 5,
            "booking_id": booking.id,
            "score": 4.5,
            "comment": "Nice activity.",
            "date": now,
            "user": user,
            "booking": booking
        }
    )

    print("user:", user.model_dump(mode="json"))
    print("booking:", booking.model_dump(mode="json"))
    print("review:", review.model_dump(mode="json"))
