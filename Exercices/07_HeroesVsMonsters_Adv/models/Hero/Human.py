from abstract.AbstractHero import AbstractHero

class Human(AbstractHero):
    @property
    def stamina(self):
        return super().stamina + 1

    @property
    def strength(self):
        return super().strength + 1