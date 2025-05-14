from typing import TypeVar, List, Callable

from newDSL.constraint.Comparator import Comparator
from newDSL.constraint.Constraint import Constraint
from newDSL.operator.Operator import Operator
from newDSL.operator.clustering.GroupingOperator import GroupingOperator
from newDSL.operator.selection.filter.FilterOperator import FilterOperator
from newDSL.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator
from newDSL.operator.selection.sampling.automatic.RandomSelectionPartitionOperator import \
    RandomSelectionPartitionOperator
from newDSL.operator.selection.sampling.automatic.SystematicRandomSelectionOperator import \
    SystematicRandomSelectionOperator
from newDSL.operator.selection.sampling.automatic.SystematicSelectionOperator import SystematicSelectionOperator
from newDSL.operator.selection.sampling.manual.InteractiveManualSamplingOperator import \
    InteractiveManualSamplingOperator
from newDSL.operator.selection.sampling.manual.ManualSamplingOperator import ManualSamplingOperator

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