
from train.ORM.models.user import User
from train.ORM.models.booking import Booking

from train.ORM.initialize import db

def batch_operation():

    """
    If everything inside begin() succeeds → auto commit

    If any exception → auto rollback

    This way, either both actions succeed or none do
    """
    try:
        with db.session.begin():

            # Get user
            user = db.session.query(User).filter_by(
                authentication_id="x6rxa6aPug"
            ).first()

            if not user:
                raise ValueError("User not found")

            # Assume your User model has bookings_count field
            # Increment makeBooking counter
            user.bookings_count += 1

            # Create makeBooking
            new_booking = Booking(
                user_id=user.id,
                activity_id=1
            )

            db.session.add(new_booking)

        print("Both operations succeeded")

    except Exception as e:
        print("Transaction failed:", e)