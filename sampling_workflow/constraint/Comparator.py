from abc import ABC, abstractmethod
from typing import TypeVar

from sampling_workflow.element.Element import Element
from sampling_workflow.metadata.Metadata import Metadata

T = TypeVar("T")


class Comparator[T](ABC):
    def __init__(self, targeted_metadata: Metadata[T]):
        self.targeted_metadata = targeted_metadata

    @abstractmethod
    def compare(self, a: Element, b: Element) -> int:
        pass
