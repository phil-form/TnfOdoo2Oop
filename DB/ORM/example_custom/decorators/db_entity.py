from models.db_column import DbColumn
from orm import entities, connection, get_cursor

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

        def __find_all(self):
            table_name = getattr(self, "__table_name__", None)
            if table_name is None:
                raise Exception("Le champs __table_name__ est obligatoire !")

            cur = get_cursor()
            cur.execute(f"SELECT * FROM {table_name}")
            data = cur.fetchall()

            return data

        cls.find_all = __find_all

        entities.append(cls)
        return cls
    return entity