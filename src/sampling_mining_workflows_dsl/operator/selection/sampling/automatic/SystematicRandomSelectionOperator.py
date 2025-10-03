from sampling_mining_workflows_dsl.operator.Operator import Operator
from sampling_mining_workflows_dsl.operator.selection.sampling.automatic.AutomaticSamplingOperator import (
    AutomaticSamplingOperator,
)
from sampling_mining_workflows_dsl.Workflow import Workflow


class SystematicRandomSelectionOperator(AutomaticSamplingOperator):
    def __init__(self, workflow: Workflow, cardinality: int, pas: int):
        super().__init__(workflow, cardinality)
        self.pas = pas

    def execute(self) -> Operator:
        raise NotImplementedError("Unimplemented method 'execute'")
