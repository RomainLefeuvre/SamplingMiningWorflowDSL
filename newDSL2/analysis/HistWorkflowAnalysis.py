from typing import TypeVar

from newDSL2.Workflow import Workflow
from newDSL2.analysis.HistAnalysis import HistAnalysis
from newDSL2.analysis.WorkflowAnalysis import WorkflowAnalysis
from newDSL2.metadata.Metadata import Metadata
from newDSL2.operator.clustering.GroupingOperator import GroupingOperator

T = TypeVar('T')

class HistWorkflowAnalysis(WorkflowAnalysis):

    def __init__(self, metadata: Metadata[T]):
        super().__init__()
        self.metadata = metadata

    def analyze(self, workflow: Workflow):
        print("analyse workflow")
        # analysis = HistAnalysis(self.metadata)
        # analysis.analyze(workflow.get_root().get_input())

        op = workflow.get_root()
        analysis = HistAnalysis(self.metadata)
        analysis.analyze(op.get_input())

        while op is not None:
            analysis.analyze(op.get_output())
            op = op.get_next_operator()
