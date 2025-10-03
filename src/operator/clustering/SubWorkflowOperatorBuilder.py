from typing import TYPE_CHECKING, TypeVar, cast

from src.constraint.BoolConstraintString import BoolConstraintString
from src.constraint.Constraint import Constraint
from src.operator.clustering.GroupingOperator import GroupingOperator
from src.operator.OperatorBuilder import OperatorBuilder
from src.operator.selection.filter.FilterOperator import FilterOperator
from src.operator.selection.sampling.automatic.RandomSelectionOperator import (
    RandomSelectionOperator,
)
from src.operator.selection.sampling.manual.ManualSamplingOperator import (
    ManualSamplingOperator,
)
from src.Workflow import Workflow

if TYPE_CHECKING:
    from src.operator.Operator import Operator

T = TypeVar("T")


class SubWorkflowOperatorBuilder:
    @staticmethod
    def grouping_operator(*workflows: "OperatorBuilder") -> "OperatorBuilder":
        workflows = [
            w.workflow for w in workflows
        ]  # Extract the Workflow objects from OperatorBuilder instances
        if not workflows:
            raise ValueError("At least one workflow must be provided.")

        # Create a GroupingOperator with the provided sub workflows
        grouping_operator = GroupingOperator(*workflows)

        # Add the grouping operator to the current workflow
        # self.workflow.add_operator(cast(Operator, grouping_operator))
        subWorkflow = Workflow()
        subWorkflow.add_operator(grouping_operator)
        return OperatorBuilder(subWorkflow)

    @staticmethod
    def random_selection_operator(cardinality: int, seed: int = 0) -> "OperatorBuilder":
        subWorkflow = Workflow()
        random_selection_operator = RandomSelectionOperator(
            subWorkflow, cardinality=cardinality, seed=seed
        )
        subWorkflow.add_operator(cast("Operator", random_selection_operator))
        return OperatorBuilder(subWorkflow)

    @staticmethod
    def filter_operator(constraint: str | Constraint) -> "OperatorBuilder":
        subWorkflow = Workflow()

        if isinstance(constraint, str):
            # Handle the case where the constraint is a string
            constraint_obj = BoolConstraintString(subWorkflow, constraint)
        elif isinstance(constraint, Constraint):
            # Handle the case where the constraint is already a Constraint object
            constraint_obj = constraint
        else:
            raise TypeError("constraint must be a string or a Constraint object")

        filter_operator = FilterOperator(subWorkflow, constraint_obj)
        subWorkflow.add_operator(cast("Operator", filter_operator))
        return OperatorBuilder(subWorkflow)

    @staticmethod
    def manual_sampling_operator(*ids: T) -> "OperatorBuilder":
        if not ids:
            raise ValueError(
                "At least one element must be provided for manual sampling."
            )

        subWorkflow = Workflow()
        manual_sampling_operator = ManualSamplingOperator(*ids)
        subWorkflow.add_operator(cast("Operator", manual_sampling_operator))
        return OperatorBuilder(subWorkflow)
