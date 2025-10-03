from typing import TypeVar

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.Set import Set
from sampling_mining_workflows_dsl.operator.Operator import Operator
from sampling_mining_workflows_dsl.operator.selection.sampling.SamplingOperator import (
    SamplingOperator,
)

T = TypeVar("T")



class UnionOperator(SamplingOperator):
    def __init__(self, workflow,indexes=[-1]):
        super().__init__(workflow)
      
    def execute(self) -> Operator:

        if self._input.get_depth() < 2:
            raise ValueError("Union Operator need a set of depth >= 2")
        if self.indexes == [-1]:
            self.indexes = list(range(self._input.size()))

        set_res = Set()
        for i in self.indexes:
            set = self._input.get_element_by_index(i)
            if not isinstance(set, Set):
                raise ValueError("Union Operator need a set of depth >= 2")
            set_res.union(set)
        return self