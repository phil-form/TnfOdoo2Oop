from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine('postgresql+psycopg2://uni:uni123@localhost:5436/university_db')
SessionFactory = sessionmaker(bind=engine)