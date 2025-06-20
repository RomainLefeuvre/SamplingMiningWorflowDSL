import abc
from typing import Generic, TypeVar

T = TypeVar('T')

class Constraint(Generic[T]):
    def __init__(self, targeted_metadata=None):
        self.targeted_metadata = targeted_metadata

    @abc.abstractmethod
    def is_satisfied(self, element):
        pass

