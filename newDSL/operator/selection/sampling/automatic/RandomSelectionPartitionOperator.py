from typing import List

from newDSL.element.Set import Set
from newDSL.operator.Operator import Operator
from newDSL.operator.selection.sampling.automatic.AutomaticSamplingOperator import AutomaticSamplingOperator

class RandomSelectionPartitionOperator(AutomaticSamplingOperator):
    def __init__(self, cardinality: int, seed: int = 0):
        super().__init__(cardinality)
        self.seed = seed

    def execute(self) -> Operator:
        from newDSL.operator.OperatorFactory import OperatorFactory  # Local import
        random_selection_operator = OperatorFactory.random_selection_operator

        self._output = Set()
        is_set_of_set = all(isinstance(x, Set) for x in self._input.get_elements())

        if is_set_of_set:
            input_sets: List[Set] = [x for x in self._input.get_elements() if isinstance(x, Set)]
            total_size = sum(len(s.get_elements()) for s in input_sets)

            # Compute the number of elements per list
            sample_sizes = [
                round((len(sublist.get_elements()) / total_size) * self._cardinality)
                for sublist in input_sets
            ]

            # Correction to ensure the total sample size matches the cardinality
            diff = self._cardinality - sum(sample_sizes)
            i = 0
            while diff != 0:
                index = i % len(input_sets)
                if diff > 0:
                    sample_sizes[index] += 1
                    diff -= 1
                else:
                    sample_sizes[index] -= 1
                    diff += 1
                i += 1

            # Generate sampled sets
            for i, sublist in enumerate(input_sets):
                cardinality = sample_sizes[i]
                sampled_set = (
                    random_selection_operator(cardinality)
                    .input_set(sublist)
                    .execute()
                    .get_output()
                )
                self._output.add_element(sampled_set)

            return self
        else:
            raise RuntimeError("Input is not a set of sets")