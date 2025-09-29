from typing import TypeVar, Type

from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.constraint.BoolConstraint import BoolConstraint

T = TypeVar("T")


class MetadataNumber(Metadata[T]):
    def __init__(self, name: str, type_: Type[T]):
        super().__init__(name, type_)

    def is_greater_than(self, value: T) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x > value, self)

    def is_greater_or_equal_than(self, value: T) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x >= value, self)

    def is_less_than(self, value: T) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x < value, self)

    def is_less_or_equal_than(self, value: T) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x <= value, self)

    def is_between(self, lower: T, upper: T) -> BoolConstraint:
        return BoolConstraint(None, lambda x: lower <= x <= upper, self)

    def is_equal(self, value: T) -> "BoolConstraint":
        return BoolConstraint(None, lambda x: x == value, self)
