from typing import TypeVar

from sampling_workflow.element.Repository import Repository
from sampling_workflow.element.Set import Set
from sampling_workflow.operator.Operator import Operator
from sampling_workflow.operator.selection.sampling.SamplingOperator import (
    SamplingOperator,
)

T = TypeVar("T")


class IntersectionOperator(SamplingOperator):
    def __init__(self, workflow,indexes=[-1]):
        super().__init__(workflow)
      
    def execute(self) -> Operator:

        if self._input.get_depth() < 2:
            raise ValueError("Intersection Operator need a set of depth >= 2")
        if self.indexes == [-1]:
            self.indexes = list(range(self._input.size()))

        set_res = Set()
        for i in self.indexes:
            set = self._input.get_element_by_index(i)
            if not isinstance(set, Set):
                raise ValueError("Intersection Operator need a set of depth >= 2")
            set_res.union(set)
        return self
