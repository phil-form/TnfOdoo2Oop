import curses
import sys

from toolBox.Display import Display
from Factories.MapFactory import MapFactory
from db.repositories.MapRepository import MapRepository
from db.repositories.HeroRepository import HeroRepository
from db.connection import Database


def main(stdscr):
    display     = Display(stdscr)
    maps_data   = MapRepository.find_all()
    heroes_data = HeroRepository.find_all()

    while True:
        mapType, size, nbMonster = display.selectMap(maps_data)
        heroData, heroName       = display.selectHero(heroes_data)

        game = MapFactory.create(mapType, size, nbMonster, display, heroData, heroName)
        game.subscribe(display)
        if not game.play():
            break

    Database.close()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure PostgreSQL is running:  docker-compose up -d")
        sys.exit(1)
