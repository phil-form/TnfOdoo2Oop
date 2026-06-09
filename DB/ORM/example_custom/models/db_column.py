from enums.db_type import DbColumnType


class DbColumn:
    def __init__(self, name: str, type: DbColumnType, primary_key: bool = False, unique: bool = False, null: bool = False):
        self.name = name
        self.type = type
        self.primary_key = primary_key
        self.unique = unique
        self.null = null