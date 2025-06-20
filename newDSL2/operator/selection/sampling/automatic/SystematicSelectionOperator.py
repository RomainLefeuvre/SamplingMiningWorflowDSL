from newDSL2.constraint.Comparator import Comparator
from newDSL2.operator.selection.sampling.automatic.AutomaticSamplingOperator import AutomaticSamplingOperator


class SystematicSelectionOperator(AutomaticSamplingOperator):
    def __init__(self, cardinality: int, order_constraint: Comparator, pas: int):
        super().__init__(cardinality)
        self.order_constraint = order_constraint