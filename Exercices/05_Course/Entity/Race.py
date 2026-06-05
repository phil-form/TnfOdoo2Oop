import threading
import time

from Entity.RaceTrack import RaceTrack
from Entity.Driver import Driver
from utils.outputs import locked_print

class Race:

    def __init__(self, name: str, circuit: RaceTrack, nbLap: int, price: int) -> None:
        self.__name = name
        self.__circuit = circuit
        self.__nbLap = nbLap
        self.__price = price
        self._concurrents = []
        self.__start_course = False
        self.__start_lock = threading.Lock()
        self.__start_lock_lock = threading.Lock()
        self._race_end_callbacks = []

    def add_race_end_callback(self, callback):
        self._race_end_callbacks.append(callback)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def circuit(self) -> RaceTrack:
        return self.__circuit

    @circuit.setter
    def circuit(self, value: RaceTrack):
        self.__circuit = value

    @property
    def nbLap(self) -> RaceTrack:
        return self.__nbLap

    @nbLap.setter
    def nbLap(self, value: int):
        self.__nbLap = value

    @property
    def price(self) -> RaceTrack:
        return self.__price

    @price.setter
    def price(self, value: int):
        if value < self.price:
            raise ValueError()

        self.__price = value

    @property
    def concurrents(self):
        return tuple(self._concurrents)

    def addDriver(self, value: Driver) -> int:
        if value != None:
            self._concurrents.append(value)
        return len(self._concurrents) - 1

    
    def startCourse(self):
        def start(concurrent: Driver, nbLap: int):
            with self.__start_lock_lock:
                n_sector = max(1, self.circuit.length // 1000)
                while True:
                    with self.__start_lock:
                        if self.__start_course:
                            break

                    time.sleep(1)

            locked_print(f"{concurrent.name} Démarre!!!")
            for i in range(nbLap * n_sector):
                concurrent.doLap(self.circuit)

        threads = []
        for concurrent in self._concurrents:
            thd = threading.Thread(target=start, args=(concurrent,self.nbLap))
            threads.append(thd)
            thd.start()

        with self.__start_lock:
            self.__start_course = True

        for thread in threads:
            thread.join()

        winner = self.getWinner()
        for cb in self._race_end_callbacks:
            cb(winner)

    def getWinner(self):
        winner = self._concurrents[0]

        for concurrent in  self._concurrents:
            locked_print(concurrent.__dict__)
            locked_print(concurrent.totalTime)
            if concurrent.totalTime < winner.totalTime:
                winner = concurrent

        return winner

    # special methods

    def __len__(self) -> int:
        return len(self._concurrents)

    def __iter__(self):
        self.current = 0
        # return self.__concurrents.__init__()
        return self

    def __next__(self):
        itr = self.current

        if itr >= len(self._concurrents):
            raise StopIteration

        self.current = itr + 1

        return self._concurrents[itr - 1]

    def __contains__(self, value):
        return True if value in self._concurrents else False

    def __getitem__(self, key):
        return self._concurrents[key]

    