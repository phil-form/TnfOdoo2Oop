from abstract.AbstractHero import AbstractHero


class Dwarf(AbstractHero):
    @property
    def stamina(self):
        return super().stamina + 2