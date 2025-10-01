from typing import TypeVar

from sampling_workflow.element.Repository import Repository
from sampling_workflow.element.Set import Set
from sampling_workflow.operator.Operator import Operator
from sampling_workflow.operator.selection.sampling.SamplingOperator import (
    SamplingOperator,
)

T = TypeVar("T")


class UnionOperator(SamplingOperator):
    def __init__(self, workflow):
        super().__init__(workflow)
      
    def execute(self) -> Operator:
        if self._input.get_depth() < 2:
            raise ValueError("Union Operator need a set of depth >= 2")
        
        self._output = Set()
        self._output = self._input.get_random_subset(self._cardinality, self._seed)
        super().execute()
        return self
