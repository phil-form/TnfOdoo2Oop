import curses
from toolBox.Display import Display
from Factories.MapFactory import MapFactory


def main(stdscr):
    display = Display(stdscr)

    while True:
        mapType, size, nbMonster = display.selectMap()
        heroRace, heroName       = display.selectHero()

        game = MapFactory.create(mapType, size, nbMonster, display, heroRace, heroName)
        game.subscribe(display)
        if not game.play():
            break


if __name__ == "__main__":
    curses.wrapper(main)
