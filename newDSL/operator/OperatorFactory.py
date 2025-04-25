from typing import TypeVar

from newDSL.constraint.Constraint import Constraint
from newDSL.operator.Operator import Operator
from newDSL.operator.clustering.GroupingOperator import GroupingOperator
from newDSL.operator.selection.filter.FilterOperator import FilterOperator
from newDSL.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator
from newDSL.operator.selection.sampling.automatic.RandomSelectionPartitionOperator import \
    RandomSelectionPartitionOperator
from newDSL.operator.selection.sampling.manual.ManualSamplingOperator import ManualSamplingOperator


T = TypeVar('T')

class OperatorFactory:
    @staticmethod
    def filter_operator(constraint: Constraint) -> FilterOperator:
        return FilterOperator(constraint)

    @staticmethod
    def random_selection_operator(cardinality: int) -> RandomSelectionOperator:
        return RandomSelectionOperator(cardinality)

    @staticmethod
    def random_selection_partition_operator(seed: int, cardinality: int) -> RandomSelectionPartitionOperator:
        return RandomSelectionPartitionOperator(cardinality = cardinality, seed = seed)

    @staticmethod
    def grouping_operator(*operators: Operator):
        return GroupingOperator(*operators)

    @staticmethod
    def manual_sampling_operator(*ids: T) -> ManualSamplingOperator[T]:
        return ManualSamplingOperator(*ids)
