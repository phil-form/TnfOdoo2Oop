from abstract.AbstractMonster import AbstractMonster
from interfaces.IGold import IGold
from interfaces.ILeather import ILeather


class Monster(AbstractMonster, IGold, ILeather):
    """
    Generic monster whose name, stat bonuses, and loot profile come from the database.
    Adding a new monster type only requires inserting a row in monster_types.

    getGold() / getLeather() always exist but return 0 when the DB row has
    drops_gold / drops_leather set to FALSE.
    """

    def __init__(self, coor, monster_data: dict) -> None:
        self._race_name    = monster_data['name']
        self.__token       = monster_data.get('token', '?').strip()
        drops_gold         = monster_data.get('drops_gold', False)
        drops_leather      = monster_data.get('drops_leather', False)
        stamina_bonus      = monster_data.get('stamina_bonus', 0)
        strength_bonus     = monster_data.get('strength_bonus', 0)
        # Bonuses forwarded to AbstractMonster (must happen before super sets health)
        super().__init__(coor, stamina_bonus, strength_bonus)
        # dice4/dice6 are now available (set by AbstractCharacter.__init__)
        self.__gold    = self.dice6.throw() if drops_gold    else 0
        self.__leather = self.dice4.throw() if drops_leather else 0

    @property
    def race(self) -> str:
        return self._race_name

    def getGold(self) -> int:
        return self.__gold

    def getLeather(self) -> int:
        return self.__leather

    def getToken(self) -> str:
        return f' {self.__token} ' if not self.hidden else ' * '
