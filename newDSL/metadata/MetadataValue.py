from typing import Generic, TypeVar

T = TypeVar('T')

class MetadataValue(Generic[T]):
    def __init__(self, metadata: 'Metadata[T]', value: T = None):
        self.metadata = metadata
        self.value = value

    def get_value(self) -> T:
        return self.value

    def get_metadata(self) -> 'Metadata[T]':
        return self.metadata

    def __str__(self) -> str:
        return str(self.value)