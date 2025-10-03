from abc import ABC, abstractmethod

from src.element.Set import Set


class Writer(ABC):
    @abstractmethod
    def write_set(self, set: Set):
        pass
