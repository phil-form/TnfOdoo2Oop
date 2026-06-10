from random import randint

from abstract.AbstractMap import AbstractMap
from Factories.MonsterFactory import MonsterFactory


class Map(AbstractMap):
    """
    Generic map whose tile token, size, and monster-weight distribution all come
    from the database.  Adding a new map type only requires rows in 'maps' and
    'map_monster_weights' — no Python code needed.
    """

    def __init__(self, size: int, nbMonster: int, display, heroData: dict,
                 heroName: str, map_config: dict) -> None:
        # Weights must be stored BEFORE super().__init__ because AbstractMap calls
        # _createMonster() during __init__ (via __initMonsters).
        self.__map_name = map_config['display_name']
        self.__weights  = map_config.get('monster_weights', [])
        super().__init__(size, nbMonster, display, heroData, heroName,
                         map_config['empty_token'])

    def _mapName(self) -> str:
        return self.__map_name

    def _createMonster(self, coord):
        return MonsterFactory.create(coord)
