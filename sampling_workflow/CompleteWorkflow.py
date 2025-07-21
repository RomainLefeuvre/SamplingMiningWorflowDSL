from typing import TypeVar



T = TypeVar('T')

class CompleteWorkflow:
    def __init__(self, workflow):
        if not workflow.is_complete():
            raise ValueError("Workflow is incomplete. Ensure it has an input, output, and at least one operator.")
        self._workflow = workflow

    def execute_workflow(self):
        self._workflow.execute_workflow()
        return self

    def analyze_workflow(self, metadata):
        self._workflow.analyze_workflow(metadata)
        return self

    def __str__(self):
        return str(self._workflow)