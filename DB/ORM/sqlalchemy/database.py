from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


class Database:
    def __init__(self, engine):
        self.engine = engine
        self.base = declarative_base()
        self.__session_factory = sessionmaker(bind=self.engine)

    def session(self):
        return self.__session_factory()

engine = create_engine('postgresql+psycopg2://app:1234@localhost:5435/test')
db = Database(engine)
