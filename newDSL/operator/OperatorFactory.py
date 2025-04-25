from newDSL.constraint.Constraint import Constraint
from newDSL.operator.selection.filter.FilterOperator import FilterOperator
from newDSL.operator.selection.sampling.automatic.RandomSelectionOperator import RandomSelectionOperator
from newDSL.operator.selection.sampling.automatic.RandomSelectionPartitionOperator import \
    RandomSelectionPartitionOperator


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

