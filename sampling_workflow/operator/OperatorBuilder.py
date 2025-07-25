from typing import cast, TypeVar

from sampling_workflow.Workflow import Workflow
from sampling_workflow.constraint.BoolConstraintString import BoolConstraintString
from sampling_workflow.constraint.Constraint import Constraint
from sampling_workflow.element.Loader import Loader
from sampling_workflow.operator.Operator import Operator
from sampling_workflow.operator.clustering.GroupingOperator import GroupingOperator
from sampling_workflow.operator.selection.filter.FilterOperator import FilterOperator
from sampling_workflow.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator
from sampling_workflow.operator.selection.sampling.manual.ManualSamplingOperator import ManualSamplingOperator

T = TypeVar('T')


class OperatorBuilder:
    def __init__(self, workflow: "Workflow"):
        self.workflow = workflow

    def grouping_operator(self, *workflows: "OperatorBuilder") -> "OperatorBuilder":
        subWorkflows = []
        for w in workflows:
            subWorkflows.append(w.workflow)
        if not workflows:
            raise ValueError("At least one workflow must be provided.")

        # Create a GroupingOperator with the provided sub workflows
        grouping_operator = GroupingOperator(self.workflow, subWorkflows)

        # Add the grouping operator to the current workflow
        self.workflow.add_operator(cast(Operator, grouping_operator))
        return self
    
    def add_metadata(self, loader: Loader) :
        self.workflow.add_metadata(loader)
        return self

    def random_selection_operator(self, cardinality: int, seed: int = 0) -> "OperatorBuilder":
        random_selection_operator = RandomSelectionOperator(self.workflow, cardinality=cardinality, seed=seed)
        self.workflow.add_operator(cast(Operator, random_selection_operator))
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
        self.workflow.add_operator(cast(Operator, filter_operator))
        return self

    def manual_sampling_operator(self, *ids: T) -> "OperatorBuilder":
        if not ids:
            raise ValueError("At least one element must be provided for manual sampling.")

        manual_sampling_operator = ManualSamplingOperator(*ids)
        self.workflow.add_operator(cast(Operator, manual_sampling_operator))
        return self

    def output(self, writer) -> "Workflow":
        return self.workflow.output(writer)
