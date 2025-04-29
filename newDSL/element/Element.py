from abc import ABC, abstractmethod
from typing import Dict, List, TypeVar
from newDSL.metadata.Metadata import Metadata
from newDSL.metadata.MetadataValue import MetadataValue

T = TypeVar('T')

class Element(ABC):
    def __init__(self):
        self.metadata: Dict[Metadata, MetadataValue] = {}

    def __hash__(self) -> int:
        return hash(frozenset(self.metadata.items()))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Element):
            return False
        return self.metadata == other.metadata

    def get_metadata_value(self, metadata: Metadata[T]) -> MetadataValue[T]:
        if metadata not in self.metadata:
            raise RuntimeError(f"Missing metadata {metadata.name}")
        return self.metadata[metadata]

    def add_metadata_values(self, metadata_values: List[MetadataValue]):
        for metadata_value in metadata_values:
            self.metadata[metadata_value.get_metadata()] = metadata_value

    def add_metadata_value(self, metadata_value: MetadataValue):
        self.metadata[metadata_value.get_metadata()] = metadata_value

    def get_all_metadata_values(self) -> Dict[Metadata, MetadataValue]:
        return self.metadata

    @abstractmethod
    def to_string(self, level: int) -> str:
        pass