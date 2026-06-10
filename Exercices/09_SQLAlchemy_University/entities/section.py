from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Section(Base):
    __tablename__ = 'section'

    section_id:   Mapped[int]       = mapped_column(Integer, primary_key=True)
    section_name: Mapped[str | None] = mapped_column(String(50))
    # use_alter=True : FK ajoutee apres creation de student (section <-> student sont circulaires)
    delegate_id:  Mapped[int | None] = mapped_column(
        Integer, ForeignKey('student.student_id', use_alter=True, name='fk_section_delegate')
    )

    delegate:   Mapped["Student"]         = relationship("Student", foreign_keys=[delegate_id])
    professors: Mapped[list["Professor"]] = relationship("Professor", back_populates="section")
    students:   Mapped[list["Student"]]   = relationship("Student", back_populates="section", foreign_keys="Student.section_id")

    def __repr__(self) -> str:
        return f"Section({self.section_id} – {self.section_name})"