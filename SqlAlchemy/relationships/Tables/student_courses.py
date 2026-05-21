


from sqlalchemy import Column, Integer,  ForeignKey, Table
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# --- create the junction table ---
student_courses = Table(
    "student_courses",
    Base.metadata,

    # student
    Column(
        "student_id",
        Integer, ForeignKey(
            "students.id", # this column links each row in 'student_courses' to a row in 'students'.
            ondelete="CASCADE", # If a student is deleted, automatically delete all student_courses rows
                                # related to this student.
        ),
        primary_key=True
    ),

    # course
    Column(
        "course_id", Integer,
        ForeignKey(
            "courses.id",  # this column links each row in 'student_courses' to a row in 'courses'.
            ondelete="CASCADE" # If a course is deleted,
                                # automatically delete all student_courses rows related to this course
        ),
        primary_key=True
    )
)