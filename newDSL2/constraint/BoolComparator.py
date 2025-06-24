from typing import Callable, Generic, TypeVar

from newDSL2.constraint.Comparator import Comparator
from newDSL2.element.Element import Element
from newDSL2.metadata.Metadata import Metadata

T = TypeVar('T')

class BoolComparator(Comparator[T], Generic[T]):
    def __init__(self, targeted_metadata: Metadata[T], comparator: Callable[[T, T], T] = None):
        super().__init__(targeted_metadata)
        self.comparator = comparator

    def compare(self, a: Element, b: Element) -> Element:
        a_value = a.get_metadata_value(self.targeted_metadata).get_value()
        b_value = b.get_metadata_value(self.targeted_metadata).get_value()
        result = self.comparator(a_value, b_value)

        return a if result == a_value else b