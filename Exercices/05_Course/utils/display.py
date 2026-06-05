from __future__ import annotations

import curses
import time
from abc import ABC, abstractmethod


DRIVER_PALETTE = [
    curses.COLOR_YELLOW,
    curses.COLOR_CYAN,
    curses.COLOR_MAGENTA,
    curses.COLOR_RED,
    curses.COLOR_GREEN,
    curses.COLOR_BLUE,
    curses.COLOR_WHITE,
]


class Colors:
    FILLED = 1
    TEXT = 2
    DIM = 3
    DIFF = 4
    HEADER = 5
    CAR = 6
    DRIVER_BASE = 10

    @classmethod
    def init(cls) -> None:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(cls.FILLED, curses.COLOR_GREEN, -1)
        curses.init_pair(cls.TEXT, curses.COLOR_WHITE, -1)
        curses.init_pair(cls.DIM, curses.COLOR_WHITE, -1)
        curses.init_pair(cls.DIFF, curses.COLOR_RED, -1)
        curses.init_pair(cls.HEADER, curses.COLOR_CYAN, -1)
        curses.init_pair(cls.CAR, curses.COLOR_YELLOW, -1)
        for i, color in enumerate(DRIVER_PALETTE):
            curses.init_pair(cls.DRIVER_BASE + i, color, -1)

    @classmethod
    def driver_pair(cls, idx: int) -> int:
        return cls.DRIVER_BASE + (idx % len(DRIVER_PALETTE))


class Screen(ABC):

    @abstractmethod
    def draw(self, stdscr, state: dict) -> None:
        pass

    @staticmethod
    def _put(stdscr, row: int, col: int, text: str, attr: int = 0) -> None:
        h, w = stdscr.getmaxyx()
        if row >= h - 1 or col >= w:
            return
        avail = w - col - 1
        if avail <= 0:
            return
        try:
            stdscr.addstr(row, col, text[:avail], attr)
        except curses.error:
            pass


class LobbyScreen(Screen):

    def draw(self, stdscr, state: dict) -> None:
        stdscr.erase()
        _, w = stdscr.getmaxyx()
        width = min(w - 1, 54)

        row = 0
        self._put(stdscr, row, 0, " LOBBY ".center(width, "─"),
                  curses.color_pair(Colors.HEADER) | curses.A_BOLD)
        row += 2

        players = state["players"]
        self._put(stdscr, row, 2, f"Pilotes inscrits ({len(players)}) :",
                  curses.color_pair(Colors.TEXT) | curses.A_BOLD)
        row += 2

        for i, name in enumerate(players, 1):
            is_me = (name == state["my_name"])
            suffix = "  <- vous" if is_me else ""
            attr = curses.color_pair(Colors.driver_pair(i - 1)) | curses.A_BOLD
            self._put(stdscr, row, 4, f"{i}.  {name}{suffix}", attr)
            row += 1

        row += 2
        if state["is_host"]:
            self._put(stdscr, row, 2, "[ESPACE]  Demarrer la course",
                      curses.color_pair(Colors.FILLED) | curses.A_BOLD)
        else:
            self._put(stdscr, row, 2, "En attente que l'hote demarre la course...",
                      curses.color_pair(Colors.DIM) | curses.A_DIM)

        row += 2
        self._put(stdscr, row, 2, "[q] quitter",
                  curses.color_pair(Colors.DIM) | curses.A_DIM)

        try:
            stdscr.refresh()
        except curses.error:
            pass


class RaceScreen(Screen):
    BAR_WIDTH = 35

    def _draw_progress_chart(self, stdscr, row: int,
                              standings: list[dict], nb_lap: int, n_sectors: int) -> int:
        ordered = sorted(standings,
                         key=lambda d: -(d["laps"] + self._overall_progress(d, n_sectors)))
        leader_laps = ordered[0]["laps"] if ordered else 0
        for i, d in enumerate(ordered, 1):
            laps = d["laps"]
            filled = min(int(laps / nb_lap * self.BAR_WIDTH), self.BAR_WIDTH) if nb_lap else 0
            driver_attr = curses.color_pair(Colors.driver_pair(d.get("color", i - 1)))

            prefix = f"  P{i}  {d['name']:<10}  "
            self._put(stdscr, row, 0, prefix, driver_attr | curses.A_BOLD)
            col = len(prefix)

            self._put(stdscr, row, col, "█" * filled, driver_attr)
            self._put(stdscr, row, col + filled,
                      "░" * (self.BAR_WIDTH - filled),
                      curses.color_pair(Colors.DIM) | curses.A_DIM)

            ic = col + self.BAR_WIDTH + 2
            self._put(stdscr, row, ic, f"{laps}/{nb_lap}", curses.color_pair(Colors.TEXT))

            diff = leader_laps - laps
            if diff > 0:
                self._put(stdscr, row, ic + 7,
                          f"  +{diff} tour{'s' if diff > 1 else ''}",
                          curses.color_pair(Colors.DIFF) | curses.A_BOLD)
            row += 1
        return row

    def _sector_sub_progress(self, d: dict) -> float:
        dur = d.get("sector_duration", 0.0)
        if dur <= 0:
            return 0.0
        return min((time.time() - d.get("sector_entry_time", time.time())) / dur, 0.99)

    def _overall_progress(self, d: dict, n_sectors: int) -> float:
        return (d.get("sector", 0) + self._sector_sub_progress(d)) / n_sectors

    @staticmethod
    def _sector_label(s: int, width: int) -> str:
        return "─" * width

    def _draw_track_chart(self, stdscr, row: int,
                           standings: list[dict], n_sectors: int) -> int:
        sector_width = max(1, self.BAR_WIDTH // n_sectors)

        ordered = sorted(standings,
                         key=lambda d: -(d["laps"] + self._overall_progress(d, n_sectors)))

        for i, d in enumerate(ordered, 1):
            sector = d.get("sector", 0)
            sub_progress = self._sector_sub_progress(d)
            driver_attr = curses.color_pair(Colors.driver_pair(d.get("color", i - 1)))

            prefix = f"  P{i}  {d['name']:<10}  "
            self._put(stdscr, row, 0, prefix, driver_attr | curses.A_BOLD)
            col = len(prefix)

            for s in range(n_sectors):
                if s < sector:
                    self._put(stdscr, row, col, "=" * sector_width, driver_attr)
                    col += sector_width

                elif s == sector:
                    filled = int(sub_progress * sector_width)
                    empty = sector_width - filled - 1
                    self._put(stdscr, row, col, "=" * filled, driver_attr)
                    col += filled
                    self._put(stdscr, row, col, "▶", driver_attr | curses.A_BOLD)
                    col += 1
                    if empty > 0:
                        self._put(stdscr, row, col, "░" * empty,
                                  curses.color_pair(Colors.DIM) | curses.A_DIM)
                        col += empty

                else:
                    self._put(stdscr, row, col, "░" * sector_width,
                              curses.color_pair(Colors.DIM) | curses.A_DIM)
                    col += sector_width

            row += 1
        return row

    def draw(self, stdscr, state: dict) -> None:
        stdscr.erase()
        _, w = stdscr.getmaxyx()
        sep_w = min(w - 1, self.BAR_WIDTH + 32)
        standings = state["standings"]
        nb_lap = state["nb_lap"]
        n_sectors = state.get("n_sectors", 1)

        row = 0
        self._put(stdscr, row, 0,
                  " AVANCEMENT GENERAL ".center(sep_w, "─"),
                  curses.color_pair(Colors.HEADER) | curses.A_BOLD)
        row += 1
        row = self._draw_progress_chart(stdscr, row, standings, nb_lap, n_sectors)

        row += 1
        self._put(stdscr, row, 0,
                  " POSITION SUR LE CIRCUIT ".center(sep_w, "─"),
                  curses.color_pair(Colors.HEADER) | curses.A_BOLD)
        row += 1
        row = self._draw_track_chart(stdscr, row, standings, n_sectors)

        if state["phase"] == "finished":
            row += 1
            self._put(stdscr, row, 0,
                      f"  *** COURSE TERMINEE  Vainqueur : {state['winner']} ***",
                      curses.color_pair(Colors.CAR) | curses.A_BOLD)

        row += 2
        self._put(stdscr, row, 0, "  [q] quitter",
                  curses.color_pair(Colors.DIM) | curses.A_DIM)

        try:
            stdscr.refresh()
        except curses.error:
            pass


class RaceDisplay:

    def __init__(self, adapter) -> None:
        self._adapter = adapter
        self._lobby_screen = LobbyScreen()
        self._race_screen = RaceScreen()

    def start(self) -> None:
        curses.wrapper(self._run)

    def _run(self, stdscr) -> None:
        curses.curs_set(0)
        stdscr.nodelay(True)
        Colors.init()

        self._adapter.start_recv()

        while True:
            key = stdscr.getch()
            state = self._adapter.get_state()

            if key == ord("q"):
                raise SystemExit(0)

            if state["phase"] == "lobby":
                if key == ord(" ") and state["is_host"]:
                    self._adapter.send_start()
                self._lobby_screen.draw(stdscr, state)
            else:
                self._race_screen.draw(stdscr, state)
                if state["phase"] == "finished":
                    time.sleep(5)
                    break

            time.sleep(0.1)
