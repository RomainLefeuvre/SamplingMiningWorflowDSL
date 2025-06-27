from newDSL2.metadata.Metadata import Metadata
from newDSL2.constraint.BoolConstraint import BoolConstraint

class MetadataNumber(Metadata[float]):
    def __init__(self, name: str):
        super().__init__(name, float)

    def is_greater_than(self, value: float) -> BoolConstraint:
        return BoolConstraint(lambda x: x > value, self)

    def is_less_than(self, value: float) -> BoolConstraint:
        return BoolConstraint(lambda x: x < value, self)

    def is_between(self, lower: float, upper: float) -> BoolConstraint:
        return BoolConstraint(lambda x: lower <= x <= upper, self)