import os
import pickle
from abc import ABC
from typing import Optional, Union

from newDSL.element.Loader import Loader
from newDSL.element.Set import Set
from newDSL.element.Writter import Writter

class Operator(ABC):
    def __init__(self):
        self._input: Optional[Set] = None
        self._output: Optional[Set] = None
        self._output_writter: Optional[Writter] = None
        self._next_operator: Optional["Operator"] = None
        self._previous_operator: Optional["Operator"] = None

    def add_metadata(self, loader) -> "Operator":
        loader.load_metadata(self._output)
        return self

    def execute(self) -> "Operator":
        if self._next_operator:
            self._next_operator._input = self._output
            self._next_operator.execute()
        elif self._output_writter:
            self._output_writter.write_set(self._output)
        return self

    def get_workflow_root_operator(self) -> "Operator":
        if self._previous_operator is None:
            return self
        return self._previous_operator.get_workflow_root_operator()

    def execute_workflow(self) -> "Operator":
        root = self.get_workflow_root_operator()
        root.input_set(self._input).execute()
        return self

    def get_next_operator(self) -> Optional["Operator"]:
        return self._next_operator

    def get_output(self) -> Optional[Set]:
        return self._output

    def get_merged_output(self) -> Set:
        result = Set()
        for element in self._output.get_elements():
            if isinstance(element, Set):
                result.union(element)
        return result

    def output(self, writter: Writter) -> "Operator":
        self._output_writter = writter
        return self

    def input_set(self, input_set: Set) -> "Operator":
        self._input = input_set
        return self

    def get_input(self) -> Optional[Set]:
        return self._input

    def input(self, loader: Loader) -> "Operator":
        self._input = loader.load_set()
        return self

    def chain(self, operator: "Operator") -> "Operator":
        self._next_operator = operator
        operator._previous_operator = self
        return operator

    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, level: int = 0) -> str:
        indent = "    " * level
        double_indent = "    " * (level + 1)
        formatted_next_operator = (
            self._next_operator.to_string(level + 3) if self._next_operator else double_indent
        )

        class_name = self.__class__.__name__
        result = (
            f"{indent}{class_name}\n"
            f"{double_indent}{self.extra_to_string(level)}\n"
            f"{double_indent}input:\n"
            f"{double_indent}{self._input.to_string(level) if self._input else 'None'}\n"
            f"{double_indent}output:\n"
            f"{double_indent}{self._output.to_string(level) if self._output else 'None'}\n"
            f"{double_indent}nextOperator:\n"
            f"{formatted_next_operator}"
        )
        return result

    def extra_to_string(self, level: int) -> str:
        return ""

    def serialize(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def deserialize(path: str) -> "Operator":
        with open(path, "rb") as file:
            return pickle.load(file)