from typing import TypeVar

from sampling_workflow.analysis.HistAnalysis import HistAnalysis
from sampling_workflow.analysis.WorkflowAnalysis import WorkflowAnalysis
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.clustering.GroupingOperator import GroupingOperator

T = TypeVar("T")


class HistWorkflowAnalysis(WorkflowAnalysis):
    def __init__(
        self,
        metadata: Metadata[T],
        top_x: int = -1,
        category: bool = True,
        sort: bool = False,
    ):
        super().__init__()
        self.category = category
        self.sort = sort
        self.metadata = metadata
        self.file_path = "hist_analysis/"
        self.top_x = top_x

    def analyze(
        self, workflow, workflow_name: str = "main workflow", op_number: int = 1
    ):
        op = workflow.get_root()
        analysis = HistAnalysis(
            self.file_path, self.metadata, self.top_x, self.category, self.sort
        )
        analysis.analyze(
            op.get_input(),
            f"{self.metadata.name}_{workflow_name}_op{op_number}_input.png",
            f"Input of operator class {op.__class__.__name__}",
        )

        while op is not None:
            if isinstance(op, GroupingOperator):
                analysis.analyze(
                    op.get_merged_output(),
                    f"{self.metadata.name}_{workflow_name}_op{op_number}_output.png",
                    f"Output of operator class {op.__class__.__name__}",
                )
                for i, internal_w in enumerate(op.get_workflows(), start=1):
                    # Recursively analyze subworkflows
                    subworkflow_name = f"subworkflow {i}"
                    self.analyze(
                        internal_w, subworkflow_name, 1
                    )  # Reset operator numbering for subworkflows
            else:
                analysis.analyze(
                    op.get_output(),
                    f"{self.metadata.name}_{workflow_name}_op{op_number}_output.png",
                    f"Output of operator class {op.__class__.__name__}",
                )
            op = op.get_next_operator()
            op_number += 1
