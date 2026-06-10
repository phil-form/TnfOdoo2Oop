from models.Monster import Monster
from db.repositories.MonsterRepository import MonsterRepository
from toolBox.Dice import Dice


class MonsterFactory:
    _cache: dict = {}
    _nb_monter_types: int = None

    @classmethod
    def _get(cls) -> dict:
        if cls._nb_monter_types is None:
            cls._nb_monter_types = len(MonsterRepository.find_all())

        monster_type_id = Dice(cls._nb_monter_types).throw()
        if monster_type_id not in cls._cache:
            cls._cache[monster_type_id] = MonsterRepository.find_by_id(monster_type_id)
        return cls._cache[monster_type_id]

    @staticmethod
    def create(coord):
        data = MonsterFactory._get()
        return Monster(coord, data)
