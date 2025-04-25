from __future__ import annotations
from abc import ABCMeta, abstractmethod

from bidouille.Operator import Operator


class Builder(metaclass=ABCMeta):

    @property
    @abstractmethod
    def operator(self) -> None:
        pass

    @abstractmethod
    def filterOperator(self, constraint) -> None:
        pass

    @abstractmethod
    def build(self) -> [Operator]:
        pass