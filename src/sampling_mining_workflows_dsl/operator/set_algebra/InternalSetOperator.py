from typing import TypeVar

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.Set import Set
from sampling_mining_workflows_dsl.operator.Operator import Operator
from sampling_mining_workflows_dsl.operator.selection.sampling.SamplingOperator import (
    SamplingOperator,
)

T = TypeVar("T")


class InternalSetOperator(SamplingOperator):
    set_function = None
    def __init__(self, workflow,indexes=[-1]):
        self.indexes
        super().__init__(workflow)
        
      
    def execute(self) -> Operator:

        if self._input.get_depth() < 2:
            raise ValueError(f" Internal set Operator need a set of depth >= 2")
        
        if not self._output.size()==0:
            print("Warning: output set is not empty, clearing it")
            self._output.remove_all_elements()

        if self.indexes == [-1]:
            self.indexes = list(range(self._input.size()))

        #get the first set and delete it from the list
        set_res = self._input.get_element_by_index(self.indexes.pop(0))
        
        for i in self.indexes:
            set = self._input.get_element_by_index(i)
            if not isinstance(set, Set):
                raise ValueError("Internal set Operator need need a set of depth >= 2")
            self.set_function(set_res,set)
        return self
    
   