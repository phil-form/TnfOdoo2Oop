from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Professor(Base):
    __tablename__ = 'professor'

    professor_id:        Mapped[int]      = mapped_column(Integer, primary_key=True)
    professor_name:      Mapped[str]      = mapped_column(String(30))
    professor_surname:   Mapped[str]      = mapped_column(String(30))
    section_id:          Mapped[int]      = mapped_column(Integer, ForeignKey('section.section_id'))
    professor_office:    Mapped[int]      = mapped_column(Integer)
    professor_email:     Mapped[str]      = mapped_column(String(30))
    professor_hire_date: Mapped[datetime] = mapped_column(DateTime)
    professor_wage:      Mapped[int]      = mapped_column(Integer)

    section: Mapped["Section"]        = relationship("Section", back_populates="professors")
    courses: Mapped[list["Course"]]   = relationship("Course",  back_populates="professor")

    def __repr__(self) -> str:
        return f"Professor({self.professor_id} – {self.professor_surname} {self.professor_name})"