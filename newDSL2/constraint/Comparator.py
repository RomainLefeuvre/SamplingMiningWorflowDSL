from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from newDSL2.element.Element import Element
from newDSL2.metadata.Metadata import Metadata

T = TypeVar('T')

class Comparator(ABC, Generic[T]):
    def __init__(self, targeted_metadata: Metadata[T]):
        self.targeted_metadata = targeted_metadata

    @abstractmethod
    def compare(self, a: Element, b: Element) -> Element:
        pass