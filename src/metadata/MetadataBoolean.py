from src.constraint.BoolConstraint import BoolConstraint
from src.metadata.Metadata import Metadata


class MetadataBoolean(Metadata[bool]):
    def __init__(self, name: str):
        super().__init__(name, bool)

    def is_true(self) -> BoolConstraint:
        return BoolConstraint(lambda x: x, self)

    def is_false(self) -> BoolConstraint:
        return BoolConstraint(lambda x: not x, self)

