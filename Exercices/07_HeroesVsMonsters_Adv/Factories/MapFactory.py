from models.Map.Forest import Forest
from models.Map.Cave import Cave


class MapFactory:
    @staticmethod
    def create(mapType="forest", size=15, nbMonster=15, display=None, heroRace=1, heroName="Hero"):
        if mapType == "forest":
            return Forest(size, nbMonster, display, heroRace, heroName)
        if mapType == "cave":
            return Cave(size, nbMonster, display, heroRace, heroName)
        raise ValueError(f"Unknown map type: {mapType}")
