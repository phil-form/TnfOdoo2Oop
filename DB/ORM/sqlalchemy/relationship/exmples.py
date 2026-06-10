import sqlalchemy as db
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped


class Base(DeclarativeBase):
    pass

#############################################
# ONE TO MANY
#############################################
class Author(Base):
    __tablename__ = 'author'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = db.Column(db.String(100), nullable=False)

    # One To Many
    authod_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('author.id'))

    author: Mapped["Author"] = relationship(back_populates='books')

#############################################
# MANY TO MANY
#############################################

enrolment = Table(
    "enrolment",
    Base.metadata,
    db.Column("student_id", db.ForeignKey("student.id"), primary_key=True),
    db.Column("course_id", db.ForeignKey("course.id"), primary_key=True),
)

class Student(Base):
    __tablename__ = 'student'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)

    courses: Mapped[list["Course"]] = relationship(secondary=enrolment, back_populates="students")

class Course(Base):
    __tablename__ = 'course'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)

    students: Mapped[list["Student"]] = relationship(secondary=enrolment, back_populates="courses")


engine = db.create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

student = Student(
    name="asdf"
)

session_factory = db.orm.sessionmaker(bind=engine)
session = session_factory()
session.add(student)

course = Course(name="qwer")

session.add(course)
student.courses.append(course)

session.commit()

# stmt = db.select(Student).where(Student.name == "asdf")
stmt = db.select(Student)
for row in session.scalars(stmt):
    print(row.__dict__)