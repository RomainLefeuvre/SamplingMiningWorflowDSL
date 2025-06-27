from newDSL2.metadata.Metadata import Metadata
from newDSL2.constraint.BoolConstraint import BoolConstraint

class MetadataString(Metadata[str]):
    def __init__(self, name: str):
        super().__init__(name, str)

    def is_equal(self, value: str) -> BoolConstraint:
        return BoolConstraint(lambda x: x == value, self)