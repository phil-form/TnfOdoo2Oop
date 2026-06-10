from decimal import Decimal

from sqlalchemy import Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Course(Base):
    __tablename__ = 'course'

    course_id:    Mapped[str]     = mapped_column(String(8), primary_key=True)
    course_name:  Mapped[str]     = mapped_column(String(200))
    course_ects:  Mapped[Decimal] = mapped_column(Numeric(3, 1))
    professor_id: Mapped[int]     = mapped_column(Integer, ForeignKey('professor.professor_id'))

    professor: Mapped["Professor"]       = relationship("Professor", back_populates="courses")
    students:  Mapped[list["Student"]]   = relationship("Student",   back_populates="course")

    def __repr__(self) -> str:
        return f"Course({self.course_id} – {self.course_name})"