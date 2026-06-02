
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, UniqueConstraint, Enum
from sqlalchemy.orm import relationship

from SqlAlchemy.relationships.main import Base


class ActivityMedia(Base):
    __tablename__ = 'activities_media'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activities.id', ondelete='CASCADE'), nullable=False)
    type = Column(Enum('image', 'video', name='activity_media_type_enum'),nullable=False)
    url = Column(String(2048), nullable=False)
    order_index = Column(Integer, nullable=False)

    # NOTE - Relationships
    activity = relationship("Activity", back_populates="activity_media")


    __table_args__ = (
        CheckConstraint('order_index >= 0', name='check_nonnegative_order_index'),
        # ✅ Ensure each activity_id has unique order indexes
        UniqueConstraint('activity_id', 'order_index', name='unique_order_per_activity'),
    )
