from typing import TYPE_CHECKING, TypeVar, cast

from sampling_mining_workflows_dsl.constraint import NaturalComparator
from sampling_mining_workflows_dsl.constraint.BoolConstraintString import BoolConstraintString
from sampling_mining_workflows_dsl.constraint.Comparator import Comparator
from sampling_mining_workflows_dsl.constraint.Constraint import Constraint
from sampling_mining_workflows_dsl.element.Loader import Loader
from sampling_mining_workflows_dsl.operator.clustering.GroupingOperator import GroupingOperator
from sampling_mining_workflows_dsl.operator.selection.filter.FilterOperator import FilterOperator
from sampling_mining_workflows_dsl.operator.selection.sampling.automatic.RandomSelectionOperator import (
    RandomSelectionOperator,
)
from sampling_mining_workflows_dsl.operator.selection.sampling.automatic.SystematicSelectionOperator import (
    SystematicSelectionOperator,
)
from sampling_mining_workflows_dsl.operator.selection.sampling.manual.ManualSamplingOperator import (
    ManualSamplingOperator,
)

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.operator.Operator import Operator
    from sampling_mining_workflows_dsl.Workflow import Workflow

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

    def set_output_set_id(self, set_id: str) -> "OperatorBuilder":
        if self.workflow.operators:
            last_operator = self.workflow.operators[-1]
            last_operator.set_output_set_id(set_id)
        return self
    
    def set_input_set_id(self, set_id: str) -> "OperatorBuilder":
        if self.workflow.operators:
            first_operator = self.workflow.operators[0]
            first_operator.set_input_set_id(set_id)
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
