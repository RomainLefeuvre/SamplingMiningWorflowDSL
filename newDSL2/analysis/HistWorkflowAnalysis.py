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
        self.file_path = "analysis/hist_saves"

    def analyze(self, workflow: Workflow, workflow_name: str = "main workflow", op_number: int = 1):
        op = workflow.get_root()
        analysis = HistAnalysis(self.metadata, self.file_path)
        analysis.analyze(op.get_input(), f"{workflow_name}_op{op_number}_input.png", f"Input of operator class {op.__class__.__name__}")

        while op is not None:
            if isinstance(op, GroupingOperator):
                # Analyze the merged output of a GroupingOperator
                analysis.analyze(op.get_merged_output(), f"{workflow_name}_op{op_number}_output.png", f"Output of operator class {op.__class__.__name__}")
                for i, internal_w in enumerate(op.get_workflows(), start=1):
                    # Recursively analyze subworkflows
                    subworkflow_name = f"subworkflow {i}"
                    self.analyze(internal_w, subworkflow_name, 1)  # Reset operator numbering for subworkflows
            else:
                # Analyze the output of a non-grouping operator
                analysis.analyze(op.get_output(), f"{workflow_name}_op{op_number}_output.png", f"Output of operator class {op.__class__.__name__}")
            op = op.get_next_operator()
            op_number += 1