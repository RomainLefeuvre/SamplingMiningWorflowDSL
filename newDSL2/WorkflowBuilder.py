from newDSL2.Workflow import Workflow
from newDSL2.operator.Operator import Operator
from newDSL2.operator.OperatorBuilder import OperatorBuilder


class WorkflowBuilder:
    def __init__(self):
        self.workflow = Workflow()

    def input(self, loader) -> "OperatorBuilder":
        self.workflow.input(loader)
        return OperatorBuilder(self.workflow)

