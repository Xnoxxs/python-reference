
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from train.ORM.relationships.tables.student_courses import student_courses

# --- setup base ---
Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # many-to-many relation via the junction
    courses = relationship(
        "Course",   # tells SQLAlchemy this relationship connects to the "Course" model
        secondary=student_courses,  # tells it which junction table to use
        back_populates="students"   # must match the variable name in "Course" model
       """
         back_populates creates a two-way link between related models,
         so that both sides stay automatically in sync when you change one.
       """
    )