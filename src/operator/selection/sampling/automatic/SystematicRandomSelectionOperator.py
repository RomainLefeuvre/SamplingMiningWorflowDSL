from src.operator.Operator import Operator
from src.operator.selection.sampling.automatic.AutomaticSamplingOperator import (
    AutomaticSamplingOperator,
)
from src.Workflow import Workflow


class SystematicRandomSelectionOperator(AutomaticSamplingOperator):
    def __init__(self, workflow: Workflow, cardinality: int, pas: int):
        super().__init__(workflow, cardinality)
        self.pas = pas

    def execute(self) -> Operator:
        raise NotImplementedError("Unimplemented method 'execute'")
