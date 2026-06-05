from abc import ABC, abstractmethod

class IObserver(ABC):
    @abstractmethod
    def update(self, event, data):
        pass
