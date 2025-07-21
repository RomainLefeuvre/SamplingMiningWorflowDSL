from typing import TypeVar, List, Callable

from sampling_workflow.constraint.Comparator import Comparator
from sampling_workflow.constraint.Constraint import Constraint
from sampling_workflow.operator.Operator import Operator
from sampling_workflow.operator.clustering.GroupingOperator import GroupingOperator
from sampling_workflow.operator.selection.filter.FilterOperator import FilterOperator
from sampling_workflow.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator
from sampling_workflow.operator.selection.sampling.automatic.RandomSelectionPartitionOperator import \
    RandomSelectionPartitionOperator
from sampling_workflow.operator.selection.sampling.automatic.SystematicRandomSelectionOperator import \
    SystematicRandomSelectionOperator
from sampling_workflow.operator.selection.sampling.automatic.SystematicSelectionOperator import SystematicSelectionOperator
from sampling_workflow.operator.selection.sampling.manual.InteractiveManualSamplingOperator import \
    InteractiveManualSamplingOperator
from sampling_workflow.operator.selection.sampling.manual.ManualSamplingOperator import ManualSamplingOperator

T = TypeVar('T')

class OperatorFactory:
    @staticmethod
    def filter_operator(constraint: Constraint) -> FilterOperator:
        return FilterOperator(constraint)

    @staticmethod
    def random_selection_operator(cardinality: int, seed: int = 0) -> RandomSelectionOperator:
        return RandomSelectionOperator(cardinality, seed)

    @staticmethod
    def random_selection_partition_operator(seed: int, cardinality: int) -> RandomSelectionPartitionOperator:
        return RandomSelectionPartitionOperator(cardinality = cardinality, seed = seed)

    @staticmethod
    def grouping_operator(*operators: Operator):
        return GroupingOperator(*operators)

    @staticmethod
    def manual_sampling_operator(*ids: T) -> ManualSamplingOperator[T]:
        return ManualSamplingOperator(*ids)

    @staticmethod
    def interactive_manual_sampling_operator() -> InteractiveManualSamplingOperator[T]:
        return InteractiveManualSamplingOperator()

    @staticmethod
    def systematic_selection_operator(cardinality: int, order_constraint: Comparator, pas: int) -> SystematicSelectionOperator:
        return SystematicSelectionOperator(cardinality, order_constraint, pas)

    @staticmethod
    def systematic_random_selection_operator(cardinality: int, pas: int) -> SystematicRandomSelectionOperator:
        return SystematicRandomSelectionOperator(cardinality, pas)

    @staticmethod
    def parameterized_operators(operator: Callable[[T], Operator], *values: T) -> List[Operator]:
        return [operator(value) for value in values]