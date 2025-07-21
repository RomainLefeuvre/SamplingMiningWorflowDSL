from sampling_workflow.Workflow import Workflow
from sampling_workflow.constraint.Comparator import Comparator
from sampling_workflow.operator.selection.sampling.automatic.AutomaticSamplingOperator import AutomaticSamplingOperator


class SystematicSelectionOperator(AutomaticSamplingOperator):
    def __init__(self, workflow:Workflow,cardinality: int, order_constraint: Comparator, pas: int):
        super().__init__(workflow, cardinality)
        self.order_constraint = order_constraint