from models.Hero import Hero


class HeroFactory:
    @staticmethod
    def create(hero_data: dict, name: str, coord):
        return Hero(name, coord, hero_data)
