import os
import pickle
from typing import Optional, Union
from newDSL.element.Set import Set

class Operator:
    def __init__(self):
        self._input = None
        self._output = None
        self._output_writer = None
        self._next_operator: Optional['operator'] = None
        self._previous_operator: Optional['operator'] = None

    def add_metadata(self, loader):
        loader.load_metadata(self._output)
        return self

    def execute(self):
        if self._next_operator:
            self._next_operator._input = self._output
            self._next_operator.execute()
        elif self._output_writer:
            self._output_writer.write_set(self._output)
        return self

    def get_workflow_root_operator(self):
        if self._previous_operator is None:
            return self
        else:
            return self._previous_operator.get_workflow_root_operator()

    def execute_workflow(self):
        root = self.get_workflow_root_operator()
        root.input_set(self._input).execute()
        return self

    def get_next_operator(self):
        return self._next_operator

    def get_output(self):
        return self._output

    def get_merged_output(self):
        result = Set()
        for element in self._output.get_elements():
            if isinstance(element, Set):
                result.union(element)
        return result

    def output(self, writer):
        self._output_writer = writer
        return self

    def input_set(self, input_set):
        self._input = input_set
        return self

    def get_input(self):
        return self._input

    def input(self, loader):
        self._input = loader.load_set()
        return self

    def chain(self, operator: 'operator'):
        self._next_operator = operator
        operator._previous_operator = self
        return operator

    def __str__(self):
        return self.to_string(0)

    def to_string(self, level: int):
        indent = "    " * level
        double_indent = "    " * (level + 1)
        formatted_next_operator = (
            self._next_operator.to_string(level + 3) if self._next_operator else double_indent
        )

        class_name = self.__class__.__name__
        result = (
            f"{indent}{class_name}\n"
            f"{double_indent}input:\n"
            f"{double_indent}{self._input}\n"
            f"{double_indent}output:\n"
            f"{double_indent}{self._output}\n"
            f"{double_indent}nextOperator:\n"
            f"{formatted_next_operator}"
        )
        return result

    def extra_to_string(self, level: int):
        return ""

    def serialize(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def deserialize(path: str) -> 'operator':
        with open(path, 'rb') as file:
            return pickle.load(file)