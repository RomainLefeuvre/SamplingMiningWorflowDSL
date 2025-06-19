from typing import Optional
from bidouille.test.Element import Element

class Operator:
    def __init__(self):
        self._input: Optional[Element] = None
        self._output: Optional[Element] = None
        self._next_operator: Optional["Operator"] = None
        self._previous_operator: Optional["Operator"] = None

    def set_op_input(self, input_element: Element) -> "Operator":
        self._input = input_element
        return self

    def set_op_output(self, output_element: Element) -> "Operator":
        self._output = output_element
        return self

    def __str__(self):
        return self.__class__.__name__
