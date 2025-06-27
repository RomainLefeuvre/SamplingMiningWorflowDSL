from abc import abstractmethod, ABC

from newDSL2.element.Set import Set


class Writter(ABC):

    @abstractmethod
    def write_set(self, set: Set):
        pass