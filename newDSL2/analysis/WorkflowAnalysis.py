from abc import ABC, abstractmethod
from newDSL2.Workflow import Workflow

class WorkflowAnalysis(ABC):
    @abstractmethod
    def analyze(self, workflow: Workflow):
        pass


