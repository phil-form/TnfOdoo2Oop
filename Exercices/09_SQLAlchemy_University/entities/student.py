from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Student(Base):
    __tablename__ = 'student'

    student_id:  Mapped[int]            = mapped_column(Integer, primary_key=True)
    first_name:  Mapped[str | None]     = mapped_column(String(50))
    last_name:   Mapped[str | None]     = mapped_column(String(50))
    birth_date:  Mapped[datetime | None] = mapped_column(DateTime)
    login:       Mapped[str | None]     = mapped_column(String(50))
    section_id:  Mapped[int | None]     = mapped_column(Integer, ForeignKey('section.section_id'))
    year_result: Mapped[int | None]     = mapped_column(Integer)
    course_id:   Mapped[str | None]     = mapped_column(String(6), ForeignKey('course.course_id'))

    section: Mapped["Section"] = relationship("Section", back_populates="students", foreign_keys=[section_id])
    course:  Mapped["Course"]  = relationship("Course",  back_populates="students")

    def __repr__(self) -> str:
        return f"Student({self.student_id} – {self.first_name} {self.last_name})"