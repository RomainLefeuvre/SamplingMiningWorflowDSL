from src.operator.OperatorBuilder import OperatorBuilder
from src.Workflow import Workflow


class WorkflowBuilder:
    def __init__(self):
        self.workflow = Workflow()

    def input(self, loader) -> "OperatorBuilder":
        self.workflow.input(loader)
        return OperatorBuilder(self.workflow)
