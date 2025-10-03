from typing import TypeVar

from sampling_mining_workflows_dsl.constraint.Comparator import Comparator
from sampling_mining_workflows_dsl.element.Element import Element

T = TypeVar("T")


class NaturalComparator[T](Comparator[T]):
    """
    Generic comparator for any type T that supports < and >.
    """

    def compare(self, a: Element, b: Element) -> int:
        va = self.targeted_metadata.extract(a)
        vb = self.targeted_metadata.extract(b)
        return (va > vb) - (va < vb)
