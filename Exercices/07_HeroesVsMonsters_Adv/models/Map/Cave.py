from abstract.AbstractMap import AbstractMap
from Factories.MonsterFactory import MonsterFactory
from toolBox.Dice import Dice


class Cave(AbstractMap):
    """Dragon-heavy dungeon: 25% Wolf, 25% Orc, 50% Dragon."""

    def __init__(self, size=12, nbMonster=12, display=None, heroRace=1, heroName="Hero"):
        super().__init__(size, nbMonster, display, heroRace, heroName)

    def _createMonster(self, coord):
        roll = Dice(4).throw()
        return MonsterFactory.create(min(roll, 3), coord)

    def _emptyToken(self):
        return ' : '
