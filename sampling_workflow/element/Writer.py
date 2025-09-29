from abc import ABC, abstractmethod

from sampling_workflow.element.Set import Set


class Writer(ABC):
    @abstractmethod
    def write_set(self, set: Set):
        pass
