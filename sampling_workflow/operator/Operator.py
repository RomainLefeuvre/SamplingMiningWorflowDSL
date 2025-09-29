import os
import pickle
from abc import ABC
from typing import TYPE_CHECKING, Optional

from sampling_workflow.element.Loader import Loader
from sampling_workflow.element.Set import Set
from sampling_workflow.element.Writer import Writer

if TYPE_CHECKING:
    from sampling_workflow.metadata import MetadataValue


class Operator(ABC):
    def __init__(self, worflow):
        self.workflow = worflow
        self._input: Set | None = None
        self._output: Set | None = None
        self._output_writter: Writer | None = None
        self._next_operator: Operator | None = None
        self._previous_operator: Operator | None = None
        # Loader to add metadata on output during the execution
        self._loader: Loader | None = None

    def add_metadata_loader(self, loader) -> "Operator":
        self._loader = loader
        return self

    def add_metadata(self) -> "Operator":
        # Add the new metadata to the existing workflow metadata list
        for metadata in self._loader.metadatas.values():
            if metadata != self._loader.metadata_id_name:
                self.workflow.add_metadata_type(metadata)

        # Load new metadata set
        new_metadata_set: Set = self._loader.load_set()
        # Add metadata value to current output set
        for element in self._output.get_elements():
            if not isinstance(element, Set):
                id = element.get_id()
                try:
                    new_element = new_metadata_set.get_element(id)
                    metadata_values: list[MetadataValue] = (
                        new_element.get_all_metadata_values().values()
                    )
                    metadata_values_filtered = [
                        x for x in metadata_values if x.get_value() != id
                    ]
                    element.add_metadata_values(metadata_values_filtered)

                except ValueError:
                    print(f"Element with id {id} not found in the metadata set")

    def execute(self) -> "Operator":
        if self._loader:
            self.add_metadata()

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

    def get_output(self) -> Set | None:
        return self._output

    def get_merged_output(self) -> Set:
        result = Set()
        for element in self._output.get_elements():
            if isinstance(element, Set):
                # Recursively flatten nested Sets
                result.elements.extend(element.flatten_set().get_elements())
            else:
                # Add non-Set elements directly
                result.add_element(element)
        return result

    def output(self, writter: Writer) -> "Operator":
        self._output_writter = writter
        return self

    def input_set(self, input_set: Set) -> "Operator":
        self._input = input_set
        return self

    def output_set(self, output_set: Set) -> "Operator":
        self._output = output_set
        return self

    def get_input(self) -> Set | None:
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
            self._next_operator.to_string(level + 3)
            if self._next_operator
            else double_indent
        )

        class_name = self.__class__.__name__
        return (
            f"{indent}{class_name}\n"
            f"{double_indent}{self.extra_to_string(level)}\n"
            f"{double_indent}input:\n"
            f"{double_indent}{self._input.to_string(level + 2) if self._input else 'None'}\n"
            f"{double_indent}output:\n"
            f"{double_indent}{self._output.to_string(level + 2) if self._output else 'None'}\n"
            f"{double_indent}nextOperator:\n"
            f"{formatted_next_operator}"
        )

    def extra_to_string(self, level: int) -> str:
        return ""

    def serialize(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def deserialize(path: str) -> "Operator":
        with open(path, "rb") as file:
            return pickle.load(file)
