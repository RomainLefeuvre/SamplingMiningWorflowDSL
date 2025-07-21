from typing import TypeVar

from sampling_workflow.analysis.HistAnalysis import HistAnalysis
from sampling_workflow.analysis.WorkflowAnalysis import WorkflowAnalysis
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.clustering.GroupingOperator import GroupingOperator

T = TypeVar('T')
class HistWorkflowAnalysis(WorkflowAnalysis):

    def __init__(self, metadata: Metadata[T],top_x: int = -1,sort: bool = False):
        super().__init__()
        self.sort = sort
        self.metadata = metadata
        self.top_x = top_x

    def analyze(self, workflow):
        from sampling_workflow.Workflow import Workflow
        op = workflow.get_root()
        analysis = HistAnalysis(self.metadata,self.top_x,self.sort)
        analysis.analyze(op.get_input(), f"Input of operator class {op.__class__.__name__}")

        while op is not None:
            if isinstance(op, GroupingOperator):
                analysis.analyze(op.get_merged_output(), f"Output of operator class {op.__class__.__name__}")
                for internal_w in op.get_workflows():
                    self.analyze(internal_w)
            else:
                analysis.analyze(op.get_output(), f"Output of operator class {op.__class__.__name__}")
            op = op.get_next_operator()