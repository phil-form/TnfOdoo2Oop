from datetime import datetime

from sqlalchemy import select

from database import Base, engine, SessionFactory
from entities.section import Section
from entities.professor import Professor
from entities.course import Course
from entities.student import Student
from entities.grade import Grade

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = SessionFactory()

# Les sections sont inserees sans delegate_id : on ne peut pas referencer
# des etudiants qui n'existent pas encore (FK circulaire section <-> student)
session.add_all([
    Section(section_id=1010, section_name='BSc Management'),
    Section(section_id=1020, section_name='MSc Management'),
    Section(section_id=1110, section_name='BSc Economics'),
    Section(section_id=1120, section_name='MSc Economics'),
    Section(section_id=1310, section_name='BA Sociology'),
    Section(section_id=1320, section_name='MA Sociology'),
])
session.commit()

session.add_all([
    Professor(professor_id=1, professor_name='zidda',     professor_surname='pietro',    section_id=1020, professor_office=402, professor_email='pzidda',     professor_hire_date=datetime(2004, 12, 11), professor_wage=1900),
    Professor(professor_id=2, professor_name='decrop',    professor_surname='alain',     section_id=1120, professor_office=403, professor_email='adecrop',    professor_hire_date=datetime(2003,  5,  9), professor_wage=1950),
    Professor(professor_id=3, professor_name='giot',      professor_surname='pierre',    section_id=1310, professor_office=404, professor_email='pgiot',      professor_hire_date=datetime(2002, 12, 21), professor_wage=2100),
    Professor(professor_id=4, professor_name='lecourt',   professor_surname='christelle',section_id=1310, professor_office=406, professor_email='clecourt',   professor_hire_date=datetime(2003,  5,  7), professor_wage=1750),
    Professor(professor_id=5, professor_name='scheppens', professor_surname='georges',   section_id=1020, professor_office=410, professor_email='gscheppens', professor_hire_date=datetime(1986, 10,  9), professor_wage=2450),
    Professor(professor_id=6, professor_name='louveaux',  professor_surname='francois',  section_id=1110, professor_office=407, professor_email='flouveaux',  professor_hire_date=datetime(1990,  5,  7), professor_wage=2200),
])
session.commit()

session.add_all([
    Course(course_id='EG1010', course_name='Derivatives',                           course_ects=3.0, professor_id=3),
    Course(course_id='EG1020', course_name='Marketing management',                  course_ects=3.5, professor_id=2),
    Course(course_id='EG2110', course_name='Marketing engineering',                 course_ects=4.0, professor_id=1),
    Course(course_id='EG2120', course_name='Financial Management',                  course_ects=4.0, professor_id=3),
    Course(course_id='EG2210', course_name='Supply chain management et e-business', course_ects=2.5, professor_id=5),
])
session.commit()

session.add_all([
    Student(student_id=1,  first_name='Georges',    last_name='Lucas',           birth_date=datetime(1944,  5, 17), login='glucas',    section_id=1320, year_result=10, course_id='EG2210'),
    Student(student_id=2,  first_name='Clint',      last_name='Eastwood',        birth_date=datetime(1930,  5, 31), login='ceastwoo',  section_id=1010, year_result=4,  course_id='EG2210'),
    Student(student_id=3,  first_name='Sean',       last_name='Connery',         birth_date=datetime(1930,  8, 25), login='sconnery',  section_id=1020, year_result=12, course_id='EG2110'),
    Student(student_id=4,  first_name='Robert',     last_name='De Niro',         birth_date=datetime(1943,  8, 17), login='rde niro',  section_id=1110, year_result=3,  course_id='EG2210'),
    Student(student_id=5,  first_name='Kevin',      last_name='Bacon',           birth_date=datetime(1958,  7,  8), login='kbacon',    section_id=1120, year_result=16, course_id=None),
    Student(student_id=6,  first_name='Kim',        last_name='Basinger',        birth_date=datetime(1953, 12,  8), login='kbasinge',  section_id=1310, year_result=19, course_id=None),
    Student(student_id=7,  first_name='Johnny',     last_name='Depp',            birth_date=datetime(1963,  6,  9), login='jdepp',     section_id=1110, year_result=11, course_id='EG2210'),
    Student(student_id=8,  first_name='Julia',      last_name='Roberts',         birth_date=datetime(1967, 10, 28), login='jroberts',  section_id=1120, year_result=17, course_id=None),
    Student(student_id=9,  first_name='Natalie',    last_name='Portman',         birth_date=datetime(1981,  6,  9), login='nportman',  section_id=1010, year_result=4,  course_id='EG2210'),
    Student(student_id=10, first_name='Georges',    last_name='Clooney',         birth_date=datetime(1961,  5,  6), login='gclooney',  section_id=1020, year_result=4,  course_id='EG2110'),
    Student(student_id=11, first_name='Andy',       last_name='Garcia',          birth_date=datetime(1956,  4, 12), login='agarcia',   section_id=1110, year_result=19, course_id=None),
    Student(student_id=12, first_name='Bruce',      last_name='Willis',          birth_date=datetime(1955,  3, 19), login='bwillis',   section_id=1010, year_result=6,  course_id='EG2210'),
    Student(student_id=13, first_name='Tom',        last_name='Cruise',          birth_date=datetime(1962,  7,  3), login='tcruise',   section_id=1020, year_result=4,  course_id='EG2110'),
    Student(student_id=14, first_name='Reese',      last_name='Witherspoon',     birth_date=datetime(1976,  3, 22), login='rwithers',  section_id=1020, year_result=7,  course_id='EG1020'),
    Student(student_id=15, first_name='Sophie',     last_name='Marceau',         birth_date=datetime(1966, 11, 17), login='smarceau',  section_id=1110, year_result=6,  course_id=None),
    Student(student_id=16, first_name='Sarah',      last_name='Michelle Gellar', birth_date=datetime(1977,  4, 14), login='smichell',  section_id=1020, year_result=7,  course_id='EG2110'),
    Student(student_id=17, first_name='Alyssa',     last_name='Milano',          birth_date=datetime(1972, 12, 19), login='amilano',   section_id=1110, year_result=7,  course_id=None),
    Student(student_id=18, first_name='Jennifer',   last_name='Garner',          birth_date=datetime(1972,  4, 17), login='jgarner',   section_id=1120, year_result=18, course_id=None),
    Student(student_id=19, first_name='Michael J.', last_name='Fox',             birth_date=datetime(1969,  6, 20), login='mfox',      section_id=1310, year_result=3,  course_id=None),
    Student(student_id=20, first_name='Tom',        last_name='Hanks',           birth_date=datetime(1956,  7,  9), login='thanks',    section_id=1020, year_result=8,  course_id='EG2110'),
    Student(student_id=21, first_name='David',      last_name='Morse',           birth_date=datetime(1953, 10, 11), login='dmorse',    section_id=1110, year_result=2,  course_id=None),
    Student(student_id=22, first_name='Sandra',     last_name='Bullock',         birth_date=datetime(1964,  7, 26), login='sbullock',  section_id=1010, year_result=2,  course_id='EG1020'),
    Student(student_id=23, first_name='Keanu',      last_name='Reeves',          birth_date=datetime(1964,  9,  2), login='kreeves',   section_id=1020, year_result=10, course_id='EG2210'),
    Student(student_id=24, first_name='Shannen',    last_name='Doherty',         birth_date=datetime(1971,  4, 12), login='sdoherty',  section_id=1320, year_result=2,  course_id='EG2120'),
    Student(student_id=25, first_name='Halle',      last_name='Berry',           birth_date=datetime(1966,  8, 14), login='hberry',    section_id=1320, year_result=18, course_id='EG2210'),
])
session.commit()

delegates = {1010: 12, 1020: 9, 1110: 15, 1120: 6, 1310: 23, 1320: 6}
for section in session.scalars(select(Section)):
    section.delegate_id = delegates[section.section_id]
session.commit()

session.add_all([
    Grade(grade='IG', lower_bound=0,  upper_bound=7),
    Grade(grade='I',  lower_bound=8,  upper_bound=9),
    Grade(grade='F',  lower_bound=10, upper_bound=11),
    Grade(grade='S',  lower_bound=12, upper_bound=13),
    Grade(grade='B',  lower_bound=14, upper_bound=15),
    Grade(grade='TB', lower_bound=16, upper_bound=17),
    Grade(grade='E',  lower_bound=18, upper_bound=20),
])
session.commit()

print("Professeurs et leur section")
for prof in session.scalars(select(Professor)):
    print(f"  {prof}  ->  {prof.section}")

print("Cours avec leur professeur")
for course in session.scalars(select(Course)):
    print(f"  {course}  ({course.course_ects} ECTS)  ->  {course.professor}")

print("Delegues par section")
for section in session.scalars(select(Section)):
    print(f"  {section}  ->  delegue : {section.delegate}")

print("Etudiants de MSc Management")
stmt = select(Student).join(Student.section).where(Section.section_name == 'MSc Management')
for student in session.scalars(stmt):
    cours = str(student.course) if student.course else 'aucun'
    print(f"  {student}  (resultat : {student.year_result}, cours : {cours})")

print("Table des mentions")
for grade in session.scalars(select(Grade)):
    print(f"  {grade}")

session.close()