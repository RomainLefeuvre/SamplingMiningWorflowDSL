from sampling_workflow.Workflow import Workflow
from sampling_workflow.operator.Operator import Operator
from sampling_workflow.operator.selection.sampling.automatic.AutomaticSamplingOperator import (
    AutomaticSamplingOperator,
)


class SystematicRandomSelectionOperator(AutomaticSamplingOperator):
    def __init__(self, workflow: Workflow, cardinality: int, pas: int):
        super().__init__(workflow, cardinality)
        self.pas = pas

    def execute(self) -> Operator:
        raise NotImplementedError("Unimplemented method 'execute'")
