from typing import TypeVar, Generic

from newDSL2.element.Repository import Repository
from newDSL2.operator.Operator import Operator
from newDSL2.operator.selection.sampling.manual.ManualSamplingOperator import ManualSamplingOperator
from newDSL2.element.Set import Set

T = TypeVar('T')

class InteractiveManualSamplingOperator(ManualSamplingOperator, Generic[T]):
    def __init__(self):
        super().__init__()

    def execute(self) -> Operator:
        self._output = Set()

        print(f"input : \n{self._input.to_string() if self._input else 'None'}")
        for element in self._input.get_elements():
            if isinstance(element, Repository):
                user_input = input(f"Do you want to keep the project with ID {element.get_id()}? (yes/no/stop): ").strip().lower()
                if user_input in {"yes", "y"}:
                    self._output.add_element(element)
                elif user_input in {"stop"}:
                    return self
            else:
                raise RuntimeError("Interactive manual sampling not implemented for sets")

        return self