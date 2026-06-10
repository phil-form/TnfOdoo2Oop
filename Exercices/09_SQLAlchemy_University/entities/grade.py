from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Grade(Base):
    __tablename__ = 'grade'

    grade:       Mapped[str] = mapped_column(String(2), primary_key=True)
    lower_bound: Mapped[int] = mapped_column(Integer)
    upper_bound: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"Grade({self.grade} : {self.lower_bound}–{self.upper_bound})"