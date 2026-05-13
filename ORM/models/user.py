from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ARRAY, CheckConstraint
from app.models.base.base import Base
from sqlalchemy.orm import relationship
from app.models.variables.variables import UTC_NOW_SERVER_DEFAULT

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    authentication_id = Column(String(128), unique=True, nullable=False)

    name = Column(String(120), nullable=False)
    email = Column(String(320), unique=True)
    password = Column(String(255))
    created = Column(TIMESTAMP(timezone=True), server_default=UTC_NOW_SERVER_DEFAULT, nullable=False)

    photo = Column(String(512))
    push_notifications_permission = Column(Boolean, default=True, nullable=False)

    devices_tokens = Column(ARRAY(String(255)), nullable=False)

    # NOTE - Relationships
    # All the activities that this user selected as his favourite
    user_favourite_activity = relationship(
        "UserFavouriteActivity",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # A user may or may not be an owner profile (1-1 optional).
    owner = relationship(
        "Owner",
        back_populates="user",
        uselist=False,
    )
    bookings = relationship("Booking", back_populates="user")
    feedbacks = relationship("FeedBack", back_populates="user")
    users_deleted = relationship("DeletedUser", back_populates="user")


    __table_args__ = (
        CheckConstraint("cardinality(devices_tokens) <= 20", name="check_max_device_tokens"),
    )

