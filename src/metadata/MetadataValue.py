from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from sampling_workflow.metadata.Metadata import Metadata

T = TypeVar("T")


class MetadataValue[T]:
    def __init__(self, metadata: "Metadata[T]", value: T = None):
        self.metadata = metadata
        self.value = value

    def get_value(self) -> T:
        return self.value

    def get_metadata(self) -> "Metadata[T]":
        return self.metadata

    def __str__(self) -> str:
        return str(self.value)

    def to_string(self) -> str:
        return self.value.to_string()
