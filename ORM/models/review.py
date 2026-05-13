

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Numeric, CheckConstraint
from app.models.base.base import Base
from app.models.variables.variables import UTC_NOW_SERVER_DEFAULT
from sqlalchemy.orm import relationship

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)

    # one-to-one with makeBooking
    booking_id = Column(Integer,ForeignKey('bookings.id', ondelete="CASCADE"), unique=True, nullable=False)

    # now allows 0 – 5 with up-to-one-decimal precision
    score = Column(Numeric(2, 1), nullable=False)   # e.g. 4, 4.5, 2.0 …

    comment = Column(String(400))
    date = Column(TIMESTAMP(timezone=True), server_default=UTC_NOW_SERVER_DEFAULT, nullable=False)

    # NOTE - Relationships
    booking = relationship("Booking", back_populates="review")

    @property
    def user(self):
        return self.booking.user if self.booking else None

    __table_args__ = (

        # score must be between 0 and 5
        CheckConstraint('score >= 0 AND score <= 5', name='score_range_check'),

    )
