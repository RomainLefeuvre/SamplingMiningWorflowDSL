from typing import TypeVar

from src.element.Repository import Repository
from src.element.Set import Set
from src.operator.Operator import Operator
from src.operator.selection.sampling.manual.ManualSamplingOperator import (
    ManualSamplingOperator,
)
from src.Workflow import Workflow

T = TypeVar("T")


class InteractiveManualSamplingOperator[T](ManualSamplingOperator):
    def __init__(self, workflow: Workflow):
        super().__init__(workflow)

    def execute(self) -> Operator:
        self._output = Set()

        print(f"input : \n{self._input.to_string() if self._input else 'None'}")
        for element in self._input.get_elements():
            if isinstance(element, Repository):
                user_input = (
                    input(
                        f"Do you want to keep the project with ID {element.get_id()}? (yes/no/stop): "
                    )
                    .strip()
                    .lower()
                )
                if user_input in {"yes", "y"}:
                    self._output.add_element(element)
                elif user_input in {"stop"}:
                    return self
            else:
                raise RuntimeError(
                    "Interactive manual sampling not implemented for sets"
                )

        return self
