from typing import TYPE_CHECKING, TypeVar, cast

from src.constraint import NaturalComparator
from src.constraint.BoolConstraintString import BoolConstraintString
from src.constraint.Comparator import Comparator
from src.constraint.Constraint import Constraint
from src.element.Loader import Loader
from src.operator.clustering.GroupingOperator import GroupingOperator
from src.operator.selection.filter.FilterOperator import FilterOperator
from src.operator.selection.sampling.automatic.RandomSelectionOperator import (
    RandomSelectionOperator,
)
from src.operator.selection.sampling.automatic.SystematicSelectionOperator import (
    SystematicSelectionOperator,
)
from src.operator.selection.sampling.manual.ManualSamplingOperator import (
    ManualSamplingOperator,
)

if TYPE_CHECKING:
    from src.operator.Operator import Operator
    from src.Workflow import Workflow

T = TypeVar("T")


class OperatorBuilder:
    def __init__(self, workflow: "Workflow"):
        self.workflow = workflow

    def grouping_operator(self, *workflows: "OperatorBuilder") -> "OperatorBuilder":
        if not workflows:
            raise ValueError("At least one workflow must be provided.")

        # Retrieve all metadata from the main workflow
        all_metadata = self.workflow.get_all_Metadata()

        # Ensure all subworkflows have the same metadata
        for w in workflows:
            for metadata in all_metadata:
                w.workflow.add_metadata_type(metadata)

        # Extract subworkflow objects
        subWorkflows = [w.workflow for w in workflows]

        # Create and add the GroupingOperator
        grouping_operator = GroupingOperator(self.workflow, subWorkflows)
        self.workflow.add_operator(cast("Operator", grouping_operator))
        return self

    def add_metadata(self, loader: Loader):
        self.workflow.add_metadata(loader)
        return self

    def random_selection_operator(
        self, cardinality: int, seed: int = 0
    ) -> "OperatorBuilder":
        random_selection_operator = RandomSelectionOperator(
            self.workflow, cardinality=cardinality, seed=seed
        )
        self.workflow.add_operator(cast("Operator", random_selection_operator))
        return self

    def filter_operator(self, constraint: str | Constraint) -> "OperatorBuilder":
        if isinstance(constraint, str):
            # Handle the case where the constraint is a string
            constraint_obj = BoolConstraintString(self.workflow, constraint)
        elif isinstance(constraint, Constraint):
            # Handle the case where the constraint is already a Constraint object
            constraint_obj = constraint
        else:
            raise TypeError("constraint must be a string or a Constraint object")

        filter_operator = FilterOperator(self.workflow, constraint_obj)
        self.workflow.add_operator(cast("Operator", filter_operator))
        return self

    def systematic_selection_operator(
        self,
        cardinality: int,
        metadata_name: str,
        reverse=False,
        step: int = 1,
        order_constraint: Comparator = NaturalComparator,
    ) -> "OperatorBuilder":
        systematic_selection_operator = SystematicSelectionOperator(
            self.workflow, cardinality, metadata_name, reverse, step, order_constraint
        )
        self.workflow.add_operator(cast("Operator", systematic_selection_operator))
        return self

    def manual_sampling_operator(self, *ids: T) -> "OperatorBuilder":
        if not ids:
            raise ValueError(
                "At least one element must be provided for manual sampling."
            )

        manual_sampling_operator = ManualSamplingOperator(*ids)
        self.workflow.add_operator(cast("Operator", manual_sampling_operator))
        return self

    def output(self, writer) -> "Workflow":
        return self.workflow.output(writer)
