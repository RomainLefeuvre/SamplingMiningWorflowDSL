from newDSL2.operator.Operator import Operator
from newDSL2.operator.selection.sampling.automatic.AutomaticSamplingOperator import AutomaticSamplingOperator

class SystematicRandomSelectionOperator(AutomaticSamplingOperator):
    def __init__(self, cardinality: int, pas: int):
        super().__init__(cardinality)
        self.pas = pas

    def execute(self) -> Operator:
        raise NotImplementedError("Unimplemented method 'execute'")