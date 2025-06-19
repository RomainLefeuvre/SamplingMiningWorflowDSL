from typing import List, Optional

from bidouille.test.Element import Element
from bidouille.test.FilterOperator import FilterOperator
from bidouille.test.Operator import Operator
from bidouille.test.SampleOperator import SampleOperator
from bidouille.test.Set import Set


class Workflow:
    def __init__(self):
        self._input: Optional[Set] = None
        self._output: Optional[Set] = None
        self._root: Optional[Operator] = None

    def filter_operator(self):
        filterOperator = FilterOperator()
        self.add_operator(filterOperator)
        return self

    def sample_operator(self, cardinality: int) -> "Workflow":
        sampleOperator = SampleOperator(cardinality=cardinality)
        self.add_operator(sampleOperator)
        return self

    def add_operator(self, operator: Operator):
        # If the workflow is empty, set the root operator
        if self._root is None:
            self._root = operator

        # If the workflow already has operators, append the new operator to the end
        else:
            current = self._root
            while current._next_operator is not None:
                current = current._next_operator

            operator.set_op_input(current.get_output())
            current.set_op_output(operator.get_output())
            current._next_operator = operator
            operator._previous_operator = current

    def input(self) -> "Workflow":
        input_element = Set()
        self._input = input_element
        # if self._root is not None:
        #     self._root.set_op_input(input_element)
        return self

    def output(self) -> "Workflow":
        output_element = Set()
        self._output = output_element
        return self

    def get_workflow_input(self) -> Optional[Element]:
        return self._input

    def set_workflow_output(self, output_element: Element) -> "Workflow":
        self._output = output_element
        # if self._root is not None:
        #     self._root.set_op_output(output_element)
        return self

    def get_workflow_output(self) -> Optional[Element]:
        # if self._root is not None:
        #     return self._root.get_output()
        return self._output

    def display(self):
        print(f"Workflow input : {self._input}")
        current = self._root
        print("---\nOperators : ")
        while current is not None:
            print(current)
            current = current._next_operator

        print(f"---\nWorkflow output : {self._output}")



