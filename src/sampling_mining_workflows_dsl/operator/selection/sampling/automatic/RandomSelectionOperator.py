import random

from sampling_mining_workflows_dsl.operator.Operator import Operator
from sampling_mining_workflows_dsl.operator.selection.sampling.automatic.AutomaticSamplingOperator import (
    AutomaticSamplingOperator,
)


class RandomSelectionOperator(AutomaticSamplingOperator):
    def __init__(self, workflow, cardinality: int, seed: int = -1):
        super().__init__(workflow, cardinality)
        # If seed is -1, a random seed will be generated
        if seed == -1:
            seed = random.randint(0, 1000000)

        self._seed = seed

    def execute(self) -> Operator:
        self._output = self._input.get_random_subset(self._cardinality, self._seed)
        super().execute()
        return self
