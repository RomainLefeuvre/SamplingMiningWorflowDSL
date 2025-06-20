from newDSL2.operator.Operator import Operator
from newDSL2.operator.selection.sampling.automatic.AutomaticSamplingOperator import AutomaticSamplingOperator


class RandomSelectionOperator(AutomaticSamplingOperator):
    def __init__(self, cardinality: int, seed: int = 0):
        super().__init__(cardinality)
        self._seed = seed

    def execute(self) -> Operator:
        self._output = self._input.get_random_subset(self._cardinality, self._seed)
        super().execute()
        return self