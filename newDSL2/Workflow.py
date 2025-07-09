from typing import List, Optional, cast, TypeVar

from newDSL2.CompleteWorkflow import CompleteWorkflow
from newDSL2.constraint.Constraint import Constraint
from newDSL2.element.Element import Element
from newDSL2.element.Loader import Loader
from newDSL2.element.Set import Set
from newDSL2.element.Writer import Writer
from newDSL2.metadata.Metadata import Metadata
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

    # --- Methods used for the Workflow creation ---

    def input(self, loader: Loader) -> "Workflow":
        self._input = loader.load_set()
        return self

    def output(self, writer: Writer) -> "Workflow":
        self._output_writer = writer
        last_operator = self.get_last_operator()
        if last_operator:
            last_operator.output(writer)
        return self


    def is_complete(self) -> bool:
        return self._root is not None and self._input is not None and self._output_writer is not None

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

        if self.is_complete():
            return CompleteWorkflow(self)

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


    # --- Methods used for the Workflow execution ---

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

    def analyze_workflow(self, metadata: Metadata[T]) -> "Workflow":
        from newDSL2.analysis.HistWorkflowAnalysis import HistWorkflowAnalysis
        # Perform analysis on a given metadata
        workflow_analysis = HistWorkflowAnalysis(metadata)
        workflow_analysis.analyze(self)
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




