import abc
from typing import TYPE_CHECKING, TypeVar

from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

if TYPE_CHECKING:
    from sampling_mining_workflows_dsl.Workflow import Workflow

T = TypeVar("T")


class Constraint[T]:
    def __init__(self, workflow: "Workflow", *targeted_metadatas: Metadata[T]):
        self.targeted_metadatas = targeted_metadatas
        self.workflow = workflow

    @abc.abstractmethod
    def is_satisfied(self, element):
        pass

    def set_workflow(self, workflow: "Workflow"):
        self.workflow = workflow
        return self
