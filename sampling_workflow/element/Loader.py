from abc import ABC, abstractmethod
from typing import Dict, Optional
from sampling_workflow.metadata import Metadata
from sampling_workflow.element import Set

class Loader(ABC):
    def __init__(self, *metadatas: Optional[Metadata]):
        # Assuming the first metadata is the ID, store its name for further use
        self.metadata_id_name = metadatas[0].name
        self.metadatas: Dict[str, Metadata] = {}
        for metadata in metadatas:
            self.metadatas[metadata.name] = metadata

    @abstractmethod
    def load_set(self) -> Set:
        pass