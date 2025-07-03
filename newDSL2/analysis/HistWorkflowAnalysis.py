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
        op = workflow.get_root()
        analysis = HistAnalysis(self.metadata)
        analysis.analyze(op.get_input(), f"Input of operator class {op.__class__.__name__}")

        while op is not None:
            if isinstance(op, GroupingOperator):
                analysis.analyze(op.get_merged_output(), f"Output of operator class {op.__class__.__name__}")
                for internal_w in op.get_workflows():
                    self.analyze(internal_w)
            else:
                analysis.analyze(op.get_output(), f"Output of operator class {op.__class__.__name__}")
            op = op.get_next_operator()
