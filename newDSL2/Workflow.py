from typing import List, Optional, cast

from newDSL2.constraint.Constraint import Constraint
from newDSL2.element.Element import Element
from newDSL2.element.Loader import Loader
from newDSL2.element.Set import Set
from newDSL2.element.Writter import Writter
from newDSL2.operator.Operator import Operator
from newDSL2.operator.clustering.GroupingOperator import GroupingOperator
from newDSL2.operator.selection.filter.FilterOperator import FilterOperator
from newDSL2.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator


class Workflow:
    def __init__(self):
        self._input: Optional[Set] = None
        self._output: Optional[Set] = None
        self._output_writter: Optional[Writter] = None
        self._root: Optional[Operator] = None

    def grouping_operator(self, *workflows: "Workflow") -> "Workflow":
        if not workflows:
            raise ValueError("At least one workflow must be provided.")

        # Extract root operators from each workflow
        operators = [workflow._root for workflow in workflows if workflow._root is not None]

        if not operators:
            raise ValueError("All provided workflows must have a root operator.")

        # Create a grouping operator with the extracted operators
        grouping_operator = GroupingOperator(*operators)

        # Add the grouping operator to the current workflow
        self.add_operator(cast(Operator, grouping_operator))
        return self

    def random_selection_operator(self, cardinality: int, seed: int = 0) -> "Workflow":
        randomSelectionOperator = RandomSelectionOperator(cardinality=cardinality, seed=seed)
        self.add_operator(cast(Operator, randomSelectionOperator))
        return self

    def filter_operator(self, constraint: Constraint):
        filterOperator = FilterOperator(constraint)
        self.add_operator(cast(Operator, filterOperator))
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

            operator.input_set(current.get_output())
            current.output_set(operator.get_output())
            current._next_operator = operator
            operator._previous_operator = current

    def input(self, loader: Loader) -> "Workflow":
        self._input = loader.load_set()
        return self

    def output(self, writter: Writter) -> "Workflow":
        self._output_writter = writter
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

    def execute_workflow(self) -> "Workflow":
        root = self._root
        root.input_set(self._input).execute()
        return self

    def display(self):
        print(self._root)
        # print(f"Workflow input : {self._input}")
        # current = self._root
        # print("---\nOperators : ")
        # while current is not None:
        #     print(current)
        #     current = current._next_operator
        #
        # print(f"---\nWorkflow output : {self._output}")



