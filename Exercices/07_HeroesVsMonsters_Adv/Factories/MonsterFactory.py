from models.Monster.Wolf import Wolf
from models.Monster.Orc import Orc
from models.Monster.Dragon import Dragon

class MonsterFactory:
    @staticmethod
    def create(monsterType: int, coord):
        if monsterType == 1:
            return Wolf(coord)
        if monsterType == 2:
            return Orc(coord)
        return Dragon(coord)
