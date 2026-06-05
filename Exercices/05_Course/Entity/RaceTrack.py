import threading

class RaceTrack:
    def __init__(self, name: str, length: int, maxPlace: int) -> None:
        self.name = name
        self.maxPlace = maxPlace
        self.__lock = threading.Lock()
        self.length = length

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def length(self):
        with self.__lock:
            return self.__length

    @length.setter
    def length(self, value: int):
        with self.__lock:
            self.__length = value

    @property
    def nbPlace(self):
        return self.__nbPlace

    @nbPlace.setter
    def nbPlace(self, value: int):
        self.__nbPlace = value

    def __str__(self) -> str:
        return f"{self.name} : {self.length}"