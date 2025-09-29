from typing import Generic, TypeVar
from sampling_workflow.constraint.Comparator import Comparator
from sampling_workflow.element.Element import Element

T = TypeVar("T")


class NaturalComparator(Comparator[T], Generic[T]):
    """
    Generic comparator for any type T that supports < and >.
    """

    def compare(self, a: Element, b: Element) -> int:
        va = self.targeted_metadata.extract(a)
        vb = self.targeted_metadata.extract(b)
        return (va > vb) - (va < vb)
