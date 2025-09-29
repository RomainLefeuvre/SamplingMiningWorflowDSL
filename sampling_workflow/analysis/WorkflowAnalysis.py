from abc import ABC, abstractmethod


class WorkflowAnalysis(ABC):
    @abstractmethod
    def analyze(self, workflow):
        pass
