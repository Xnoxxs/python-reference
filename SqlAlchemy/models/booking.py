
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint,
    Enum,
)
from app.models.base.base import Base
from app.models.variables.variables import UTC_NOW_SERVER_DEFAULT
from sqlalchemy.orm import relationship

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)

    activity_id = Column(Integer, ForeignKey('activities.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    slot_id = Column(Integer, ForeignKey('activity_slots.id', ondelete="CASCADE"), nullable=True)

    schedule_type = Column(Enum('slots', 'days', name='booking_type_enum'), nullable=False)

    people = Column(Integer, nullable=False)

    # "pending" | "success" | "failed"
    # pending if user hasn't yet made payment
    # failed if user made payment, but transaction wasn't added to db_setup because of an error
    # success if user made payment and transaction was added to db_setup
    status = Column(Enum('pending', 'success', 'failed', 'canceled', name='booking_status_enum'),nullable=False)

    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    reservation_date = Column(TIMESTAMP(timezone=True), server_default=UTC_NOW_SERVER_DEFAULT, nullable=False)

    activity_price = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)

    code = Column(String(32), unique=True, nullable=False)

    asked_for_rating = Column(Boolean, default=False, nullable=False)

    # NOTE - Relationships
    activity = relationship("Activity", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
    activity_slot = relationship("ActivitySlot", back_populates="bookings")
    review = relationship("Review", back_populates="booking", uselist=False, cascade="all, delete-orphan")


    __table_args__ = (
        # start_date must be before end_date
        CheckConstraint('start_date < end_date', name='check_start_before_end'),

        # reservation_date must be before start_date AND end_date
        CheckConstraint('reservation_date < start_date AND reservation_date < end_date',
                        name='check_reservation_before_dates'),

        # slot_id must exist for slots and be NULL for days
        CheckConstraint(
            "(schedule_type = 'slots' AND slot_id IS NOT NULL) OR "
            "(schedule_type = 'days' AND slot_id IS NULL)",
            name='check_slot_dependency'
        ),

        # ensure positive values for counts and monetary amounts
        CheckConstraint('people > 0', name='check_positive_people'),
        CheckConstraint('activity_price >= 0', name='check_activity_price_non_negative'),
        CheckConstraint('total_price >= 0', name='check_total_price_non_negative'),
        CheckConstraint('total_price >= activity_price', name='check_total_price_bounds'),
    )


