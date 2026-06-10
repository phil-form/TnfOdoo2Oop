from models.Map import Map
from db.repositories.MapRepository import MapRepository


class MapFactory:
    @staticmethod
    def create(mapType: str, size: int, nbMonster: int, display, heroData: dict, heroName: str):
        map_config = MapRepository.find_by_type(mapType)
        if map_config is None:
            raise ValueError(f"Map type '{mapType}' not found in database")
        return Map(size, nbMonster, display, heroData, heroName, map_config)
