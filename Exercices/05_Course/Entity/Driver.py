import threading
import time

from Entity.Car import Car
from Entity.RaceTrack import RaceTrack
from utils.outputs import locked_print


class Driver:

    def __init__(self, name: str, number: int, car: Car) -> None:
        self.__name = name
        self.__number = number
        self.__car = car
        self.__sector_times: list[float] = []
        self.__lapTime: list[float] = []

        self.__lap_callbacks = []
        self.__sector_callbacks = []

        self.__n_sectors = 1
        self.__current_sector = 0
        self.__sector_entry_time = 0.0
        self.__last_sector_duration = 0.0

    def add_lap_callback(self, callback):
        self.__lap_callbacks.append(callback)

    def add_sector_callback(self, callback):
        self.__sector_callbacks.append(callback)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def number(self) -> int:
        return self.__number

    @number.setter
    def number(self, value: int):
        self.__number = value

    @property
    def car(self) -> Car:
        return self.__car

    @car.setter
    def car(self, value: Car):
        self.__car = value

    @property
    def lapTimes(self) -> tuple:
        return tuple(self.__lapTime)

    @property
    def totalTime(self) -> float:
        return sum(self.lapTimes)

    @property
    def get_last_lap_time(self) -> float:
        return self.__lapTime[-1]

    @property
    def n_sectors(self) -> int:
        return self.__n_sectors

    @property
    def current_sector(self) -> int:
        return self.__current_sector

    @property
    def sector_entry_time(self) -> float:
        return self.__sector_entry_time

    @property
    def last_sector_duration(self) -> float:
        return self.__last_sector_duration

    def doLap(self, circuit: RaceTrack) -> None:
        vit = self.car.getSpeed() / 3.6
        n_sectors = max(1, circuit.length // 1000)
        distance = circuit.length / n_sectors
        sector_time = distance / vit
        self.__n_sectors = n_sectors

        # callback fired on sector entry so the display can animate within it
        self.__current_sector = (self.__current_sector + 1) % n_sectors
        self.__sector_entry_time = time.time()
        for cb in self.__sector_callbacks:
            cb(self)
        self.__last_sector_duration = sector_time
        time.sleep(sector_time / 60)

        self.__sector_times.append(sector_time)
        if len(self.__sector_times) % n_sectors == 0:
            total_lap_time = sum(self.__sector_times[-n_sectors:])
            self.__lapTime.append(total_lap_time)
            locked_print(f"{self.__name} lap time: {total_lap_time:.2f}s")
            for cb in self.__lap_callbacks:
                cb(self)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Driver):
            return self.name == other.name
        return False
