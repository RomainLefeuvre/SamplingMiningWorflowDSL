from src.constraint import NaturalComparator
from src.constraint.Comparator import Comparator
from src.operator.Operator import Operator
from src.operator.selection.sampling.automatic.AutomaticSamplingOperator import (
    AutomaticSamplingOperator,
)
from src.Workflow import Workflow


class SystematicSelectionOperator(AutomaticSamplingOperator):
    def __init__(
        self,
        workflow: Workflow,
        cardinality: int,
        metadata_name: str,
        reverse=False,
        step: int = 1,
        order_constraint: Comparator = NaturalComparator,
    ):
        super().__init__(workflow, cardinality)

        self.metadata_name = metadata_name
        self.step = step
        self.order_constraint = order_constraint

    def execute(self) -> Operator:
        self._input.sort_by_metadata(
            self.metadata_name, self.order_constraint, self.reverse
        )
        self._output = self._input.get_systematic_subset(self._cardinality, self.step)
        return self
