
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, defer, load_only, with_loader_criteria
from sqlalchemy.testing import db

from SqlAlchemy.models.activity import Activity
from SqlAlchemy.models.activity_media import ActivityMedia
from SqlAlchemy.models.booking import Booking
from SqlAlchemy.models.review import Review
from SqlAlchemy.models.user import User
from deploymentPipeline.dev import app

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
                joinedload(Booking.review).load_only(Review.score, Review.comment)
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
        #  Get user and his reviews for each booking  (relation)
        #
        # NOTE:
        #   Even though you just wanted the reviews, The reviews don't have a direct relationship
        #   to user. They have a traversing relationship. Which means that they are linked through
        #   a different relationship. They don't have one of their own.
        #   Meaning, that to get review of a user, you need to get booking first
        #   And even though you don't need booking data, the query will still get it
        #   because that is how SQL works
        # -----------------------------------
        user_bookings_with_review = (
            db.session.query(User)
            .options(
                joinedload(User.bookings).joinedload(Booking.review)
            )
            .all()
        )
        # Improved Version
        # NOTE:
        #  The question is not: "Can I avoid loading Activity?"
        #  The answer is: No.
        #  The real question is: "Can I load the minimum amount of Activity possible?"
        #  And the answer is: Yes
        #  .options(
        #     joinedload(Booking.activity)
        #         .load_only(Activity.id)
        #         .joinedload(Activity.activity_media)
        # )
        user_bookings_with_review = (
            db.session.query(User)
            .options(
                joinedload(User.bookings)
                .load_only(Booking.id).joinedload(Booking.review)
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

        # -----------------------------------
        # Get bookings with activity,
        # but only the first media (lowest id)
        # for each activity
        #
        # NOTE:
        #   Activity -> ActivityMedia is a one-to-many relationship.
        #
        #   By default:
        #
        #       joinedload(Activity.activity_media)
        #
        #   loads ALL media.
        #
        #   The loader criteria below filters the
        #   relationship so that only the media row
        #   having the smallest id for that activity
        #   is loaded.
        # -----------------------------------
        bookings_with_first_media = (
            db.session.query(Booking)
            .options(
                joinedload(Booking.activity).options(
                    load_only(Activity.id),
                    joinedload(Activity.activity_media),
                ),

                with_loader_criteria(
                    ActivityMedia,
                    ActivityMedia.id
                    == (
                        select(func.min(ActivityMedia.id))
                        .where(
                            ActivityMedia.activity_id == Activity.id
                        )
                        .correlate(Activity)
                        .scalar_subquery()
                    ),
                    include_aliases=True,
                ),
            )
            .all()
        )

        print("\nQuery Result:")
        for booking in bookings_with_first_media:
            media_ids = [
                media.id
                for media in booking.activity.activity_media
            ]

            print(
                booking.id,
                booking.activity.id,
                media_ids,
            )