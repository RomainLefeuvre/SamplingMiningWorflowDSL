from typing import TYPE_CHECKING, TypeVar

from src.constraint.Constraint import Constraint
from src.element.Element import Element
from src.metadata.Metadata import Metadata
from src.Workflow import Workflow

if TYPE_CHECKING:
    from src.constraint.BoolConstraint import BoolConstraint

T = TypeVar("T")


class BoolConstraintString(Constraint[T]):
    def __init__(
        self,
        workflow: Workflow,
        string_constraint: str,
        *targeted_metadatas: Metadata[T],
    ):
        super().__init__(workflow, *targeted_metadatas)

        self.string_constraint = string_constraint
        self.or_constraint: Constraint | None = None
        self.and_constraint: Constraint | None = None

    def set_workflow(self, workflow: Workflow):
        self.workflow = workflow
        worflow_metadatas = workflow.get_all_Metadata()
        self.targeted_metadatas = tuple(worflow_metadatas)
        return self

    def is_satisfied(self, element: Element) -> bool:
        all_metadata = self.workflow.get_all_Metadata()

        # Retrieve matching Metadata objects by checking if their names exist in the string_constraint
        matching_metadata = [
            metadata
            for metadata in all_metadata
            if metadata.name in self.string_constraint
        ]

        metadata_values = {}
        for metadata in matching_metadata:
            metadata_value = element.get_metadata_value(metadata)
            if metadata_value:
                metadata_values[metadata.name] = metadata_value.get_value()

        # Evaluate the string_constraint
        constraint_result = False
        try:
            constraint_result = eval(self.string_constraint, {}, metadata_values)
        except Exception as e:
            print(f"Error evaluating string_constraint: {e}")
        return constraint_result

    def or_(self, other: "BoolConstraint") -> "BoolConstraint":
        self.or_constraint = other
        return other

    def and_(self, other: "BoolConstraint") -> "BoolConstraint":
        self.and_constraint = other
        return other

    def get_string_constraint(self) -> str:
        return self.string_constraint
