from typing import Generic, TypeVar, List

from newDSL.element.Repository import Repository
from newDSL.element.Set import Set
from newDSL.operator.Operator import Operator
from newDSL.operator.selection.sampling.SamplingOperator import SamplingOperator

T = TypeVar('T')

class ManualSamplingOperator(SamplingOperator, Generic[T]):
    def __init__(self, *ids: T):
        super().__init__(len(ids))
        self.ids = ids

    def execute(self) -> Operator:
        self._output = Set()

        for element in self._input.get_elements():
            if isinstance(element, Repository):
                if any(element.get_id() == id_ for id_ in self.ids):
                    self._output.add_element(element)
            else:
                raise RuntimeError("Manual sampling not implemented for sets")

        return self