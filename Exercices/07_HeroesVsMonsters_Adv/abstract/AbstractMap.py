import curses
from abc import ABC

from abstract.AbstractMonster import AbstractMonster
from models.Coordinate import Coordinate
from enums.Direction import Direction
from enums.GameEvent import GameEvent
from interfaces.IGold import IGold
from interfaces.ILeather import ILeather
from interfaces.IObservable import IObservable
from toolBox.Dice import Dice
from Factories.MonsterFactory import MonsterFactory
from Factories.HeroFactory import HeroFactory


class AbstractMap(IObservable, ABC):
    def __init__(self, size, nbMonster, display, heroRace, heroName):
        super().__init__()
        self._display = display
        self._heroRace = heroRace
        self._heroName = heroName
        self.__size = size
        self.__characters = []
        self.__initMonsters(nbMonster)
        self.__hero = self._initPlayer()
        self.__characters.append(self.__hero)
        self.__ennemyCount = nbMonster

    def _initPlayer(self):
        return HeroFactory.create(self._heroRace, self._heroName, self._getValidCoord())

    def _createMonster(self, coord):
        return MonsterFactory.create(Dice(3).throw(), coord)

    def _emptyToken(self):
        return ' . '

    def _mapName(self):
        return self.__class__.__name__

    def __initMonsters(self, nbMonster):
        for _ in range(nbMonster):
            self.__characters.append(self._createMonster(self._getValidCoord()))

    def _getValidCoord(self):
        dice = Dice(self.__size)
        isPlaced = False
        while not isPlaced:
            x, y = dice.throw() - 1, dice.throw() - 1
            isPlaced = all(
                abs(c.coorX - x) >= 3 or abs(c.coorY - y) >= 3
                for c in self.__characters
            )
        return Coordinate(x, y)

    def __characterMoved(self):
        key = self._display.readKey()
        moved = False
        hero = self.__hero
        size = self.__size

        if key in (curses.KEY_UP, ord('w'), ord('W')):
            if hero.coorX > 0:
                hero.move(Direction.NORTH)
                moved = True
        elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
            if hero.coorX < size - 1:
                hero.move(Direction.SOUTH)
                moved = True
        elif key in (curses.KEY_LEFT, ord('a'), ord('A')):
            if hero.coorY > 0:
                hero.move(Direction.WEST)
                moved = True
        elif key in (curses.KEY_RIGHT, ord('d'), ord('D')):
            if hero.coorY < size - 1:
                hero.move(Direction.EAST)
                moved = True
        elif key in (ord('q'), ord('Q'), 27):
            return None

        return moved

    def __getNearestMonster(self):
        for char in self.__characters:
            if isinstance(char, AbstractMonster) and char.coorX == self.__hero.coorX and char.coorY == self.__hero.coorY:
                return char
        return None

    def __fight(self, monster: AbstractMonster):
        hero = self.__hero
        self.notify(GameEvent.FIGHT_START, f"{hero.name} vs {monster.race}!")
        monster.hidden = False

        if monster.isDead():
            return

        init = Dice(2).throw() == 1
        while not hero.isDead() and not monster.isDead():
            hero.hit(monster) if init else monster.hit(hero)
            init = not init

        if not hero.isDead():
            loot = []
            if isinstance(monster, IGold):
                loot.append(f"{monster.getGold()} gold")
            if isinstance(monster, ILeather):
                loot.append(f"{monster.getLeather()} leather")
            hero.loot(monster)
            hero.rest()
            hero.killCount += 1
            self.notify(GameEvent.KILL,
                        f"Killed {monster.race}! +{', '.join(loot) if loot else 'nothing'}")

    def __getState(self):
        return {
            'characters': self.__characters,
            'hero': self.__hero,
            'size': self.__size,
            'ennemyCount': self.__ennemyCount,
            'emptyToken': self._emptyToken(),
            'mapName': self._mapName(),
        }

    def play(self):
        self.notify(GameEvent.MAP_UPDATED, self.__getState())

        while not self.__hero.isDead() and self.__hero.killCount < self.__ennemyCount:
            result = self.__characterMoved()
            if result is None:
                break
            if result:
                self.notify(GameEvent.MAP_UPDATED, self.__getState())
                monster = self.__getNearestMonster()
                if monster is not None:
                    self.__fight(monster)
                    self.notify(GameEvent.MAP_UPDATED, self.__getState())

        if self.__hero.isDead():
            self.notify(GameEvent.GAME_OVER, "YOU DIED")
        elif self.__hero.killCount >= self.__ennemyCount:
            gold = self.__hero.getGold()
            leather = self.__hero.getLeather()
            self.notify(GameEvent.GAME_OVER, f"YOU WIN!  Gold:{gold}  Leather:{leather}")

        return self._display.askReplay()
