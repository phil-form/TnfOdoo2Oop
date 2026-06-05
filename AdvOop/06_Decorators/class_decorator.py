from enum import Enum

def simple_class_decorator(cls):
    print(cls)
    print(type(cls))
    print("Do Something")
    return cls

@simple_class_decorator
class TestDeco:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        print(self.arg1, self.arg2)

test = TestDeco("test", "test")

def class_decorator_with_args(arg1, arg2):
    def decorator(cls):
        print(f"Arguments: {arg1}, {arg2}")
        print(cls)
        print(type(cls))
        print("Do Something")
        return cls
    return decorator

@class_decorator_with_args("arg1", "arg2")
class TestDecorator2:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        print(self.arg1, self.arg2)

test = TestDecorator2("test", "test")

def entity(cls):
    # Réflexion: détecter automatiquement les attributs de type DbColumn
    __db_columns = [
        name for name, value in vars(cls).items()
        if isinstance(value, DbColumn)
    ]

    for field in __db_columns:
        private = f"_{cls.__name__}__{field}"

        def make_property(attr):
            def getter(self):
                return getattr(self, attr)
            def setter(self, value):
                setattr(self, f"_{cls.__name__}__touched", True)
                setattr(self, attr, value)
            return property(getter, setter)

        setattr(cls, field, make_property(private))

    def _init_entity(self, data=None):
        setattr(self, f"_{cls.__name__}__touched", False)
        if data is None:
            data = {}
        for field in __db_columns:
            setattr(self, f"_{cls.__name__}__{field}", data.get(field))

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

class DbColumnType(Enum):
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    CHAR = "CHAR"
    VARCHAR = "VARCHAR"

class DbColumn:
    def __init__(self, name: str, type: DbColumnType, primary_key: bool = False, unique: bool = False):
        self.name = name
        self.type = type


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

def db_entity(table_name):
    def entity(cls):
        # Réflexion: détecter automatiquement les attributs de type DbColumn
        __db_columns = [
            name for name, value in vars(cls).items()
            if isinstance(value, DbColumn)
        ]

        for field in __db_columns:
            private = f"_{cls.__name__}__{field}"

            def make_property(attr):
                def getter(self):
                    return getattr(self, attr)
                def setter(self, value):
                    setattr(self, f"_{cls.__name__}__touched", True)
                    setattr(self, attr, value)
                return property(getter, setter)

            setattr(cls, field, make_property(private))

        def _init_entity(self, data=None):
            setattr(self, f"_{cls.__name__}__touched", False)
            if data is None:
                data = {}
            for field in __db_columns:
                setattr(self, f"_{cls.__name__}__{field}", data.get(field))

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
    return entity

@db_entity("users")
class User:
    user_id = DbColumn("user_id", DbColumnType.INTEGER, primary_key=True)
    username = DbColumn("username", DbColumnType.VARCHAR, unique=True)

user = User()
print(user.__dict__)
user.user_id = 1
user.username = "test"
print(user.__dict__)
