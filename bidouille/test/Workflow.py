from typing import List, Optional

from bidouille.test.FilterOperator import FilterOperator
from bidouille.test.Operator import Operator
from bidouille.test.SampleOperator import SampleOperator


class Workflow:
    def __init__(self):
        self._root: Optional[Operator] = None

    def filter_operator(self):
        filterOperator = FilterOperator()
        self.add_operator(filterOperator)
        return self

    def sample_operator(self, cardinality: int) -> "Workflow":
        sampleOperator = SampleOperator(cardinality=cardinality)
        self.add_operator(sampleOperator)

        return self

    def add_operator(self, operator: Operator):
        if self._root is None:
            self._root = operator
        else:
            current = self._root
            while current._next_operator is not None:
                current = current._next_operator
            current._next_operator = operator
            operator._previous_operator = current

    def display(self):
        current = self._root
        while current is not None:
            print(current)
            current = current._next_operator


