from abstract.AbstractMap import AbstractMap


class Forest(AbstractMap):
    def __init__(self, size=15, nbMonster=15, display=None, heroRace=1, heroName="Hero"):
        super().__init__(size, nbMonster, display, heroRace, heroName)
