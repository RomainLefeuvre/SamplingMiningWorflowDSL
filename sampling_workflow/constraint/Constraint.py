import abc
from typing import Generic, Tuple, TypeVar

from sampling_workflow.metadata.Metadata import Metadata

T = TypeVar("T")


class Constraint(Generic[T]):
    def __init__(self, workflow: "Workflow", *targeted_metadatas: Metadata[T]):
        self.targeted_metadatas = targeted_metadatas
        self.workflow = workflow

    @abc.abstractmethod
    def is_satisfied(self, element):
        pass

    def set_workflow(self, workflow: "Workflow"):
        self.workflow = workflow
        return self
