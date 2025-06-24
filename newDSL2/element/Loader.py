from abc import ABC, abstractmethod
from typing import Dict, Optional
from newDSL2.metadata import Metadata
from newDSL2.element import Set

class Loader(ABC):
    def __init__(self, *metadatas: Optional[Metadata]):
        self.metadatas: Dict[str, Metadata] = {}
        for metadata in metadatas:
            self.metadatas[metadata.name] = metadata

    @abstractmethod
    def load_set(self) -> Set:
        pass