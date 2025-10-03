from typing import TypeVar

from sampling_workflow.element.Repository import Repository
from sampling_workflow.element.Set import Set
from sampling_workflow.operator.Operator import Operator
from sampling_workflow.operator.selection.sampling.SamplingOperator import (
    SamplingOperator,
)

T = TypeVar("T")


class ManualSamplingOperator[T](SamplingOperator):
    def __init__(self, workflow, *ids: T):
        super().__init__(workflow, len(ids))
        self.ids = ids

    def execute(self) -> Operator:
        self._output = Set()

        for element in self._input.get_elements():
            if isinstance(element, Repository):
                if any(element.get_id() == id_ for id_ in self.ids):
                    self._output.add_element(element)
            else:
                raise RuntimeError("Manual sampling not implemented for sets")
        super().execute()
        return self
