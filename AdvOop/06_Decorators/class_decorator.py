from enum import Enum


def entity(cls):
    # Réflexion: détecter automatiquement les attributs de type DbColumn
    __db_columns = [
        name for name, value in vars(cls).items()
        if isinstance(value, DbColumn)
    ]

    for field in __db_columns:
        private = f"__{field}"

        def make_property(attr):
            def getter(self):
                return getattr(self, attr)
            def setter(self, value):
                self.__touched = True
                setattr(self, attr, value)
            return property(getter, setter)

        setattr(cls, field, make_property(private))

    def _init_entity(self, data=None):
        self.__touched = False
        if data is None:
            data = {}
        for field in __db_columns:
            setattr(self, f"__{field}", data.get(field))

    def _get_entity_info(self):
        if not getattr(self, "__table_name__", None):
            raise Exception("Le champs __table_name__ est obligatoire !")

        return {
            "__table_name__": getattr(self, "__table_name__"),
            "db_fields": __db_columns
        }

    cls.__init__ = _init_entity
    cls.get_entity_info = _get_entity_info
    return cls

class DbColumn:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class DbColumnType(Enum):
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    CHAR = "CHAR"
    VARCHAR = "VARCHAR"


@entity
class Person:
    __table_name__ = "persons"

    last_name = DbColumn("last_name", DbColumnType.VARCHAR)
    first_name = DbColumn("first_name", DbColumnType.VARCHAR)
    age = DbColumn("age", DbColumnType.INTEGER)

person = Person()
print(person.__dict__)
person.last_name = "Duck"
person.first_name = "Donald"
person.age = 100
print(person.__dict__)
