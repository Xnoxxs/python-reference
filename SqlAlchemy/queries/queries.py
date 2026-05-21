
from train.ORM.initialize import app, db
from sqlalchemy import func
from sqlalchemy.orm import joinedload, defer, load_only

from train.ORM.models.user import User
from train.ORM.models.booking import Booking
from train.ORM.models.review import Review


if __name__ == "__main__":

    with app.app_context():

        # -----------------------------------
        #  Get all users
        # -----------------------------------
        users_basic = (
            db.session.query(User)
            .all()
        )

        print("\nQuery 1 Result:")
        print(users_basic)

        # -----------------------------------
        #  Get all users but only specific fields (id, name)
        # -----------------------------------
        users_specific_data = (
            db.session.query(User)
            .options(load_only(User.id, User.name))
            .all()
        )

        print("\nQuery 2 Result:")
        print(users_specific_data)

        # -----------------------------------
        # Get all users but don't include a specific field (email)
        # -----------------------------------
        users_without_email = (
            db.session.query(User)
            .options(defer(User.email))
            .all()
        )

        print("\nQuery 3 Result:")
        print(users_without_email)

        # -----------------------------------
        # Get user by primary key
        # -----------------------------------
        user_by_pk = db.session.get(User, 1)

        print("\nQuery 4 Result:")
        print(user_by_pk)

        # -----------------------------------
        # Get user by primary key (only id and name)
        # -----------------------------------
        user_by_pk_specific_data = (
            db.session.query(User.id, User.name)
            .filter(User.id == 1)
            .first()
        )

        print(user_by_pk_specific_data)


        # -----------------------------------
        #  Complex filtering + order + limit
        # -----------------------------------
        users_filtered = (
            db.session.query(User.id, User.name)
            .filter(
                User.id != 1,
                User.name.in_(["Jack", "Mark"])
            )
            .order_by(User.created.desc())  # desc: 2026 --> 2025 --> 2024
                                            # asc: 2024 --> 2025 --> 2026
            .limit(20)
            .all()
        )

        print("\nQuery 5 Result:")
        print(users_filtered)


        # -----------------------------------
        #  Get bookings with review (relation)
        # -----------------------------------
        bookings_with_review = (
            db.session.query(Booking)
            .options(joinedload(Booking.review))
            .all()
        )

        print("\nQuery Result:")
        for booking in bookings_with_review:
            review_score = booking.review.score if booking.review else None
            print(booking.id, booking.reservation_date, booking.total_price, review_score)

        # -----------------------------------
        #  Get bookings with review (relation), but only one specific field (score) from review
        # -----------------------------------
        bookings_with_review_score = (
            db.session.query(Booking)
            .options(
                joinedload(Booking.review).load_only(Review.score)
            )
            .all()
        )

        print("\nQuery Result:")
        for booking in bookings_with_review_score:
            review_score = booking.review.score if booking.review else None
            print(booking.id,review_score)


        # -----------------------------------
        # Filter bookings by related review score < 4
        # -----------------------------------
        bookings_low_review = (
            db.session.query(Booking)
            .join(Booking.review)
            .filter(Review.score < 4)
            .all()
        )

        print("\nQuery Result:")
        for booking in bookings_low_review:
            print(booking.id, booking.reservation_date, booking.total_price, booking.review.score)

        # -----------------------------------
        #  Get bookings with review and user (relation)
        # -----------------------------------
        bookings_with_review_and_user = (
            db.session.query(Booking)
            .options(
                joinedload(Booking.review),
                joinedload(Booking.user)
            )
            .all()
        )

        print("\nQuery Result:")
        for booking in bookings_with_review_and_user:
            review_score = booking.review.score if booking.review else None
            user_name = booking.user.name if booking.user else None
            print(booking.id, booking.reservation_date, booking.total_price, user_name, review_score)


        # -----------------------------------
        #  Get user with bookings and with reviews for each booking  (relation)
        # -----------------------------------
        user_bookings_with_review = (
            db.session.query(User)
            .options(
                joinedload(User.bookings).joinedload(Booking.review)
            )
            .all()
        )

        print("\nQuery Result:")
        for user in user_bookings_with_review:
            for booking in user.bookings:
                booking_price = booking.total_price
                review_score = booking.review.score if booking.review else None
                print(f"User: {user.name} - {booking_price} - {review_score}")

        # -----------------------------------
        #  Get specific booking data with user
        # -----------------------------------
        user_bookings_with_review = (
            db.session.query(User)
            .options(
                joinedload(User.bookings)
                .load_only(Booking.id,Booking.activity_price),
                joinedload(User.bookings)
                .joinedload(Booking.review)
            )
            .all()
        )


        # -----------------------------------
        # Count bookings per user
        # -----------------------------------
        users_with_booking_count = (
            db.session.query(
                User.id,
                User.name,
                func.count(Booking.id).label("booking_count")
            )
            # .outerjoin = LEFT JOIN
            .outerjoin(User.bookings)
            .group_by(User.id, User.name)
            .all()
        )

        print("\nQuery Result:")
        for row in users_with_booking_count:
            user_id, user_name, booking_count = row
            print(user_id, user_name, booking_count)