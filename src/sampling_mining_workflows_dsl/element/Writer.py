from abc import ABC, abstractmethod

from sampling_mining_workflows_dsl.element.Set import Set


class Writer(ABC):
    @abstractmethod
    def write_set(self, set: Set):
        pass
