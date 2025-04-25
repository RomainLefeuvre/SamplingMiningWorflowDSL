from __future__ import annotations
from abc import ABCMeta, abstractmethod

class Builder (metaclass=ABCMeta):

    @property
    @abstractmethod
    def sandwich(self) -> None:
        pass

    @abstractmethod
    def addBread(self) -> None:
        pass

    @abstractmethod
    def addMeat(self) -> None:
        pass

    @abstractmethod
    def addLettuce(self) -> None:
        pass

    @abstractmethod
    def addTomato(self) -> None:
        pass
