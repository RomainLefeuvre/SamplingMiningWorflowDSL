from typing import List

from bidouille.test.FilterOperator import FilterOperator
from bidouille.test.Operator import Operator
from bidouille.test.SampleOperator import SampleOperator


class Workflow:
    def __init__(self, operators: List[Operator] = None):
        self._operators = operators or []

    def filterOperator(self):
        return Workflow(self._operators + [FilterOperator()])

    def sampleOperator(self, cardinality: int):
        sampleOperator = SampleOperator(cardinality=cardinality)

        return Workflow(self._operators + [sampleOperator])

    def display(self):
        for op in self._operators:
            print(op)

    def __str__(self):
        return str([str(op) for op in self._operators])

