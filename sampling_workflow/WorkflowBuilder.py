from sampling_workflow.Workflow import Workflow
from sampling_workflow.operator.Operator import Operator
from sampling_workflow.operator.OperatorBuilder import OperatorBuilder


class WorkflowBuilder:
    def __init__(self):
        self.workflow = Workflow()

    def input(self, loader) -> "OperatorBuilder":
        self.workflow.input(loader)
        return OperatorBuilder(self.workflow)

