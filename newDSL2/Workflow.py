from typing import List, Optional, cast, TypeVar
from newDSL2.constraint.Constraint import Constraint
from newDSL2.element.Element import Element
from newDSL2.element.Loader import Loader
from newDSL2.element.Set import Set
from newDSL2.element.Writer import Writer
from newDSL2.operator.Operator import Operator
from newDSL2.operator.clustering.GroupingOperator import GroupingOperator
from newDSL2.operator.selection.filter.FilterOperator import FilterOperator
from newDSL2.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator
from newDSL2.operator.selection.sampling.manual.ManualSamplingOperator import ManualSamplingOperator

T = TypeVar('T')

class Workflow:
    def __init__(self):
        self._input: Optional[Set] = None
        self._output: Optional[Set] = None
        self._output_writer: Optional[Writer] = None
        self._root: Optional[Operator] = None
        self._last_operator: Optional[Operator] = None


    # --- Methods used for the DSL (used by the user) ---

    def grouping_operator(self, *workflows: "Workflow") -> "Workflow":
        if not workflows:
            raise ValueError("At least one workflow must be provided.")

        # Create a GroupingOperator with the provided sub workflows
        grouping_operator = GroupingOperator(*workflows)

        # Add the grouping operator to the current workflow
        self.add_operator(cast(Operator, grouping_operator))
        return self

    def random_selection_operator(self, cardinality: int, seed: int = 0) -> "Workflow":
        random_selection_operator = RandomSelectionOperator(cardinality=cardinality, seed=seed)
        self.add_operator(cast(Operator, random_selection_operator))
        return self

    def filter_operator(self, constraint: Constraint):
        filter_operator = FilterOperator(constraint)
        self.add_operator(cast(Operator, filter_operator))
        return self

    def manual_sampling_operator(self, *ids: T) -> "Workflow":
        if not ids:
            raise ValueError("At least one element must be provided for manual sampling.")

        manual_sampling_operator = ManualSamplingOperator(*ids)
        self.add_operator(cast(Operator, manual_sampling_operator))
        return self

    def input(self, loader: Loader) -> "Workflow":
        self._input = loader.load_set()
        return self

    def output(self, writer: Writer) -> "Workflow":
        self._output_writer = writer
        last_operator = self.get_last_operator()
        if last_operator:
            last_operator.output(writer)
        return self

    # --- Methods used for the Workflow execution ---

    def add_operator(self, operator: Operator):
        # If the workflow is empty, set the root operator
        if self._root is None:
            self._root = operator
            self._last_operator = operator

        # If the workflow already has operators, append the new operator to the end
        else:
            self._last_operator._next_operator = operator
            operator._previous_operator = self._last_operator
            operator.input_set(self._last_operator.get_output())
            self._last_operator.output_set(operator.get_output())
            self._last_operator = operator

    def set_workflow_input(self, input_set: Set | None) -> "Workflow":
        self._input = input_set
        if self._root is not None:
            self._root.input_set(input_set)
        return self

    def set_root_input(self, input_set: Set | None) -> "Workflow":
        if self._root is None:
            raise ValueError("Cannot set root input when no root operator is defined.")
        self._root.input_set(input_set)
        return self

    def get_workflow_input(self) -> Optional[Element]:
        return self._input

    def set_workflow_output(self, output_element: Element) -> "Workflow":
        self._output = output_element
        return self

    def get_workflow_output(self) -> Optional[Set]:
        return self._output

    def get_root(self) -> Optional[Operator]:
        return self._root

    def get_last_operator(self) -> Optional[Operator]:
        if self._root is None:
            return None
        current = self._root
        while current._next_operator is not None:
            current = current._next_operator
        return current

    def execute_workflow(self) -> "Workflow":
        root = self._root
        root.input_set(self._input)
        root.execute()
        self._output = self._last_operator.get_output()
        return self


    # --- Methods for workflow printing ---

    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, level: int):
        indent = "    " * level
        res = f"{indent}Workflow: [[[\n"
        # res = ""
        if self._root is not None:
            res += self._root.to_string(level)
        else:
            res += f"{indent}No operators defined in this workflow.\n"

        res += "\n" + indent + "]]]\n"
        return res




