import os
import pickle
from abc import ABC
from typing import Optional

from newDSL.element.Loader import Loader
from newDSL.element.Set import Set
from newDSL.element.Writter import Writter


class Operator(ABC):
    def __init__(self):
        self.input: Optional[Set] = None
        self.output: Optional[Set] = None
        self.output_writer: Optional[Writter] = None
        self.next_operator: Optional['Operator'] = None
        self.previous_operator: Optional['Operator'] = None

    def add_metadata(self, loader) -> 'Operator':
        loader.load_metadata(self.output)
        return self

    def execute(self) -> 'Operator':
        if self.next_operator:
            self.next_operator.input = self.output
            self.next_operator.execute()
        elif self.output_writer:
            self.output_writer.write_set(self.output)
        return self

    def get_workflow_root_operator(self) -> 'Operator':
        if self.previous_operator is None:
            return self
        return self.previous_operator.get_workflow_root_operator()

    def execute_workflow(self) -> 'Operator':
        root = self.get_workflow_root_operator()
        root.input_set(self.input).execute()
        return self

    def get_next_operator(self) -> Optional['Operator']:
        return self.next_operator

    def get_output(self) -> Optional[Set]:
        return self.output

    def get_merged_output(self) -> Set:
        result = Set()
        for element in self.output.get_elements():
            if isinstance(element, Set):
                result.union(element)
        return result

    def output(self, writer: Writter) -> 'Operator':
        self.output_writer = writer
        return self

    def input_set(self, input_set: Set) -> 'Operator':
        self.input = input_set
        return self

    def get_input(self) -> Optional[Set]:
        return self.input

    def input_loader(self, loader: Loader) -> 'Operator':
        self.input = loader.load_set()
        return self

    def chain(self, operator: 'Operator') -> 'Operator':
        self.next_operator = operator
        operator.previous_operator = self
        return operator

    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, level: int) -> str:
        indent = "    " * level
        double_indent = "    " * (level + 1)
        formatted_next_operator = (
            self.next_operator.to_string(level + 3) if self.next_operator else double_indent
        )

        class_name = self.__class__.__name__
        result = (
            f"{indent}{class_name}\n"
            f"{double_indent}{self.extra_to_string(level)}\n"
            f"{double_indent}input:\n"
            f"{double_indent}{self.input.to_string(level) if self.input else 'None'}\n"
            f"{double_indent}output:\n"
            f"{double_indent}{self.output.to_string(level) if self.output else 'None'}\n"
            f"{double_indent}nextOperator:\n"
            f"{formatted_next_operator}"
        )
        return result

    def extra_to_string(self, level: int) -> str:
        return ""

    def serialize(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def deserialize(path: str) -> 'Operator':
        with open(path, 'rb') as file:
            return pickle.load(file)