from abc import ABC

from abstract.AbstractCharacter import AbstractCharacter
from interfaces.IGold import IGold
from interfaces.ILeather import ILeather
from enums.Direction import Direction


class AbstractHero(AbstractCharacter, IGold, ILeather, ABC):
    def __init__(self, name, coor, stamina_bonus=0, strength_bonus=0) -> None:
        # Bonuses must be set before super().__init__ because AbstractCharacter
        # calls self.maxHealth → self.stamina during __init__.
        self._stamina_bonus = stamina_bonus
        self._strength_bonus = strength_bonus
        super().__init__(coor)

        self.__name = name
        self.__gold = 0
        self.__leather = 0
        self.__killCount = 0

    @property
    def stamina(self):
        return super().stamina * 2 + self._stamina_bonus

    @property
    def strength(self):
        return super().strength * 2 + self._strength_bonus

    @property
    def name(self):
        return self.__name

    @property
    def killCount(self):
        return self.__killCount

    @killCount.setter
    def killCount(self, value):
        self.__killCount = value

    def getGold(self):
        return self.__gold

    def getLeather(self):
        return self.__leather

    def loot(self, monster):
        self.__gold    += monster.getGold()
        self.__leather += monster.getLeather()

    def rest(self):
        self.health = self.maxHealth

    def move(self, direction: Direction):
        if direction == Direction.NORTH:
            self.coorX -= 1
        elif direction == Direction.SOUTH:
            self.coorX += 1
        elif direction == Direction.EAST:
            self.coorY += 1
        else:
            self.coorY -= 1

    def __str__(self) -> str:
        return f"{self.__name} " + super().__str__()

    def getToken(self):
        return ' H ' if not self.isDead() else ' X '
