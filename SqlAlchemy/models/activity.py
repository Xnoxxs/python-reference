import datetime

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, ARRAY, CheckConstraint, Enum

from sqlalchemy.orm import relationship

from SqlAlchemy.relationships.main import Base


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    public_id = Column(String(10), nullable=False, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey('owners.id', ondelete="CASCADE"), nullable=False)
    activity_collection_id = Column(Integer, ForeignKey('activities_collection.id', ondelete="CASCADE"), nullable=False)

    name = Column(String(160), unique=True, nullable=False)
    description = Column(String(2000), nullable=False)

    city = Column(String(80), nullable=False)
    country = Column(String(80), nullable=False)
    timezone = Column(String(64), server_default="Africa/Casablanca", nullable=False)
    location_name = Column(String(150), nullable=False)

    phone_number = Column(String(20), nullable=True)

    verified = Column(Boolean, default=False, nullable=False)

    session_duration = Column(Integer, nullable=False) # In minutes
    price = Column(Integer, nullable=False)

    schedule_type = Column(Enum('slots', 'days', name='activity_booking_type_enum'),nullable=False)

    # NOTE - RELATIONSHIPS
    owner = relationship("Owner", back_populates="activities")
    activity_media = relationship(
        "ActivityMedia",
        back_populates="activity",
        cascade="all, delete-orphan",
        order_by="ActivityMedia.order_index"  # always get the activity_media by ascending order_index (small → large)
    )
    bookings = relationship("Booking", back_populates="activity", cascade="all, delete-orphan")
    activity_slots = relationship("ActivitySlot", back_populates="activity", cascade="all, delete-orphan")
    __table_args__ = (
        CheckConstraint('price > 0', name='activities_check_price_positive'),
        CheckConstraint('session_duration > 0', name='activities_check_session_duration_positive'),
    )

    def to_dict(self, seen=None):
        if seen is None:
            seen = set()

        if id(self) in seen:
            return None
        seen.add(id(self))

        result = {}

        # Columns
        for column in self.__table__.columns:
            result[column.name] = getattr(self, column.name)

        # 👇 ONLY INCLUDE WHAT YOU WANT
        if self.owner:
            result["owner"] = {
                "id": self.owner.id,
                "user_id": self.owner.user_id
            }

        if self.activity_media:
            result["activity_media"] = [
                {
                    "id": m.id,
                    "url": m.url,
                    "order_index": m.order_index
                }
                for m in self.activity_media
            ]

        return result
