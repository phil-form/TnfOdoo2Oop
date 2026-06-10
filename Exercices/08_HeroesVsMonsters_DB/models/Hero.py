from abstract.AbstractHero import AbstractHero


class Hero(AbstractHero):
    """
    Generic hero whose race name and stat bonuses come entirely from a database row.
    Adding a new race only requires inserting a row in hero_races — no Python code needed.
    """

    def __init__(self, name: str, coor, hero_data: dict) -> None:
        self._race_name    = hero_data['name']
        stamina_bonus      = hero_data.get('stamina_bonus', 0)
        strength_bonus     = hero_data.get('strength_bonus', 0)
        super().__init__(name, coor, stamina_bonus, strength_bonus)

    @property
    def race(self) -> str:
        return self._race_name
