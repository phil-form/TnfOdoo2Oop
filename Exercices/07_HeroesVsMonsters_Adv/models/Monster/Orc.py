from abstract.AbstractMonster import AbstractMonster
from interfaces.IGold import IGold

class Orc(AbstractMonster, IGold):
    def __init__(self, coor) -> None:
        super().__init__(coor)
        self.__gold = self.dice6.throw()

    @property
    def strength(self):
        return super().strength + 1

    def getGold(self):
        return self.__gold

    def getToken(self):
        return ' O ' if not self.hidden else  ' * '