import os
import sys
import threading
import time
from sys import argv

from Entity.Car import Car
from Entity.Driver import Driver
from Entity.OnlineRace import OnlineRace
from Entity.Race import Race
from Entity.RaceTrack import RaceTrack
from utils.display import RaceDisplay
from utils.inputs import read_int

TRACKS = [
    RaceTrack("Spa", 7004,  20),
    RaceTrack("Le Mans", 13626, 20),
    RaceTrack("Nürburgring", 25378, 20),
]

AVAILABLE_CARS = [
    Car("Ferrari",  "F1", 250, 350),
    Car("Mercedes", "W12", 240, 340),
    Car("Red Bull", "RB16", 245, 345),
]


class LocalRaceAdapter:

    def __init__(self, race: Race):
        self._race = race
        self._lock = threading.Lock()
        self._standings: list[dict] = []
        self._phase = "racing"
        self._winner = None

    def start_recv(self):
        for driver in self._race.concurrents:
            driver.add_lap_callback(self._on_lap)
            driver.add_sector_callback(self._on_sector)
        self._race.add_race_end_callback(self._on_race_end)
        self._update_standings(None)
        threading.Thread(target=self._race.startCourse, daemon=True).start()

    def get_state(self) -> dict:
        with self._lock:
            return {
                "nb_lap": self._race.nbLap,
                "n_sectors": max(1, self._race.circuit.length // 1000),
                "is_host": False,
                "my_name": "",
                "phase": self._phase,
                "players": [d.name for d in self._race.concurrents],
                "standings": list(self._standings),
                "winner": self._winner,
            }

    def send_start(self):
        pass

    def _on_lap(self, driver):
        self._update_standings(driver)

    def _on_sector(self, driver):
        self._update_standings(driver)

    def _on_race_end(self, winning_driver):
        with self._lock:
            self._winner = winning_driver.name
            self._phase  = "finished"

    def _update_standings(self, _driver):
        now = time.time()
        with self._lock:
            prev = {d["name"]: d for d in self._standings}
            color_index = {d.name: i for i, d in enumerate(self._race.concurrents)}
            ordered = sorted(
                self._race.concurrents,
                key=lambda d: (-len(d.lapTimes), -d.current_sector, d.name),
            )
            data = []
            for d in ordered:
                entry = {
                    "name": d.name,
                    "laps": len(d.lapTimes),
                    "total": d.totalTime,
                    "last_lap": d.get_last_lap_time if d.lapTimes else 0.0,
                    "sector": d.current_sector,
                    "sector_entry_time": d.sector_entry_time,
                    "sector_duration": d.last_sector_duration / 60,
                    "color": color_index.get(d.name, 0),
                }
                n = entry["name"]
                if n in prev and prev[n]["laps"] == entry["laps"]:
                    entry["update_time"] = prev[n].get("update_time", now)
                else:
                    entry["update_time"] = now
                data.append(entry)
            self._standings = data


if "--online" not in argv:
    c = Race("technobel eaudooce", TRACKS[2], 50, 5000)
    c.addDriver(Driver("riri",   5, Car("Audi", "A3", 180, 260)))
    c.addDriver(Driver("fifi",   5, Car("Audi", "A3", 180, 260)))
    c.addDriver(Driver("loulou", 5, Car("Audi", "A3", 180, 260)))

    adapter = LocalRaceAdapter(c)

    # stdout → /dev/null so Race/Driver debug prints don't corrupt curses
    with open(os.devnull, "w") as devnull:
        old_stdout, sys.stdout = sys.stdout, devnull
        try:
            RaceDisplay(adapter).start()
        finally:
            sys.stdout = old_stdout

    winner = adapter.get_state()["winner"]
    if winner:
        print(f"\nVainqueur : {winner}")

else:
    for i, track in enumerate(TRACKS):
        print(f"{i + 1}. {track.name}")

    selection = read_int(msg="Select a track : ")
    track = TRACKS[selection - 1]
    online_race = OnlineRace("technobel eaudooce", track, 50, 5000, AVAILABLE_CARS)
    online_race.wait_for_completion()
