from abc import ABC, abstractmethod

from src.element import Set
from src.metadata.Metadata import Metadata


class Loader(ABC):
    def __init__(self, *metadatas: Metadata | None):
        # Assuming the first metadata is the ID, store its name for further use
        self.metadata_id_name = metadatas[0].name
        self.metadatas: dict[str, Metadata] = {}
        for metadata in metadatas:
            self.metadatas[metadata.name] = metadata

    @abstractmethod
    def load_set(self) -> Set:
        pass
