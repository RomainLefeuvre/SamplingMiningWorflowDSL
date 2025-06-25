from typing import List

from newDSL2.element.Set import Set
from newDSL2.operator.Operator import Operator


class GroupingOperator(Operator):
    def __init__(self, *workflows: "Workflow"):
        super().__init__()
        from newDSL2.Workflow import Workflow
        self.workflows: List[Workflow] = list(workflows)

    def execute(self) -> Operator:
        self._output = Set()
        for w in self.workflows:
            # The input of the workflow is the input of the grouping operator
            w.set_workflow_input(self._input)

            # Propagate the output_writer to the subworkflow
            if self._output_writter:
                w.output(self._output_writter)

            w.execute_workflow()
            self._output.union(w.get_workflow_output())
        super().execute()
        return self

    def get_workflows(self) -> List["Workflow"]:
        return self.workflows

    def extra_to_string(self, level: int) -> str:
        indent = "    " * (level + 1)
        res = f"\n{indent}Internal Workflows:"
        for w in self.workflows:
            res += f"\n{w.to_string(level + 1)}"
        return res