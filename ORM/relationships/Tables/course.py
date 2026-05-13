
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from train.ORM.relationships.tables.student_courses import student_courses

# --- setup base ---
Base = declarative_base()

# --- course model ---
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    students = relationship(
        "Student", # tells SQLAlchemy this relationship connects to the "Student" model
        secondary=student_courses, # tells it which junction table to use
        back_populates="courses" # must match the variable name in Student model
        """
        back_populates creates a two-way link between related models,
        so that both sides stay automatically in sync when you change one.
        """
    )