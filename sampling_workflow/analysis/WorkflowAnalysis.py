from abc import ABC, abstractmethod
from sampling_workflow.Workflow import Workflow

class WorkflowAnalysis(ABC):
    @abstractmethod
    def analyze(self, workflow: Workflow):
        pass


