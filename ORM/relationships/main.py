
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from train.ORM.relationships.tables.course import Course
from train.ORM.relationships.tables.student import Student

# --- setup base ---
Base = declarative_base()


def run_demo():
    # --- connect to PostgreSQL ---
    # (replace with your own connection string)
    engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/mydb")

    Base.metadata.create_all(engine)  # create all 3 tables

    # --- images some repositories ---
    student1 = Student(name="Alice")
    student2 = Student(name="Bob")

    course1 = Course(title="Math")
    course2 = Course(title="Physics")

    # link students and courses
    student1.courses.append(course1) # Alice takes course 1
    student1.courses.append(course2) # Alice takes course 2
    student2.courses.append(course1) # Bob takes course 1

    # Add them
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all([student1, student2])
    session.commit()


if __name__ == "__main__":
    run_demo()

