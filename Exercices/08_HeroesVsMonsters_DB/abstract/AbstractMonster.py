from abc import ABC
from abstract.AbstractCharacter import AbstractCharacter


class AbstractMonster(AbstractCharacter, ABC):
    def __init__(self, coord, stamina_bonus=0, strength_bonus=0) -> None:
        # Bonuses must be set before super().__init__ because AbstractCharacter
        # calls self.maxHealth → self.stamina during __init__.
        self._stamina_bonus = stamina_bonus
        self._strength_bonus = strength_bonus
        super().__init__(coord)
        self.__hidden = True

    @property
    def stamina(self):
        return super().stamina + self._stamina_bonus

    @property
    def strength(self):
        return super().strength + self._strength_bonus

    @property
    def hidden(self):
        return self.__hidden

    @hidden.setter
    def hidden(self, value: bool):
        self.__hidden = value
