from typing import cast, TypeVar

from newDSL2.Workflow import Workflow
from newDSL2.constraint.Constraint import Constraint
from newDSL2.operator.Operator import Operator
from newDSL2.operator.clustering.GroupingOperator import GroupingOperator
from newDSL2.operator.selection.filter.FilterOperator import FilterOperator
from newDSL2.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator
from newDSL2.operator.selection.sampling.manual.ManualSamplingOperator import ManualSamplingOperator

T = TypeVar('T')


class OperatorBuilder:
    def __init__(self, workflow: "Workflow"):
        self.workflow = workflow


    def grouping_operator(self, *workflows: "Workflow") -> "OperatorBuilder":
        if not workflows:
            raise ValueError("At least one workflow must be provided.")

        # Create a GroupingOperator with the provided sub workflows
        grouping_operator = GroupingOperator(*workflows)

        # Add the grouping operator to the current workflow
        self.workflow.add_operator(cast(Operator, grouping_operator))
        return self

    def random_selection_operator(self, cardinality: int, seed: int = 0) -> "OperatorBuilder":
        random_selection_operator = RandomSelectionOperator(cardinality=cardinality, seed=seed)
        self.workflow.add_operator(cast(Operator, random_selection_operator))
        return self

    def filter_operator(self, constraint: Constraint) -> "OperatorBuilder":
        filter_operator = FilterOperator(constraint)
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
