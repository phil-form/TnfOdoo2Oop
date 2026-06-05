from models.Hero.Human import Human
from models.Hero.Dwarf import Dwarf

class HeroFactory:
    @staticmethod
    def create(race: int, name: str, coord):
        if race == 1:
            return Human(name, coord)
        return Dwarf(name, coord)
