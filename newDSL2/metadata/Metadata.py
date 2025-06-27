from typing import Type, TypeVar, Callable, Generic

T = TypeVar('T')

class Metadata(Generic[T]):
    def __init__(self, name: str, type_: Type[T]):
        self.name = name
        self.type = type_

    def __hash__(self):
        return hash((self.name, self.type))

    def __eq__(self, other):
        if not isinstance(other, Metadata):
            return False
        return self.name == other.name and self.type == other.type

    def is_equal(self, value: T) -> 'BoolConstraint':
        from newDSL2.constraint.BoolConstraint import BoolConstraint
        return BoolConstraint(lambda x: x == value, self)

    def is_more_than(self, value: T) -> 'BoolConstraint':
        from newDSL2.constraint.BoolConstraint import BoolConstraint
        if not isinstance(value, (int, float)):
            raise TypeError("`is_more_than` can only be used with numeric types.")
        return BoolConstraint(lambda x: x > value, self)

    def is_more_or_equal_than(self, value: T) -> 'BoolConstraint':
        from newDSL2.constraint.BoolConstraint import BoolConstraint
        if not isinstance(value, (int, float)):
            raise TypeError("`is_more_or_equal_than` can only be used with numeric types.")
        return BoolConstraint(lambda x: x >= value, self)

    def is_less_than(self, value: T) -> 'BoolConstraint':
        from newDSL2.constraint.BoolConstraint import BoolConstraint
        if not isinstance(value, (int, float)):
            raise TypeError("`is_less_than` can only be used with numeric types.")
        return BoolConstraint(lambda x: x < value, self)

    def is_less_or_equal_than(self, value: T) -> 'BoolConstraint':
        from newDSL2.constraint.BoolConstraint import BoolConstraint
        if not isinstance(value, (int, float)):
            raise TypeError("`is_less_or_equal_than` can only be used with numeric types.")
        return BoolConstraint(lambda x: x <= value, self)

    def is_between(self, lower: T, upper: T) -> 'BoolConstraint':
        from newDSL2.constraint.BoolConstraint import BoolConstraint
        if not isinstance(lower, (int, float)) or not isinstance(upper, (int, float)):
            raise TypeError("`is_between` can only be used with numeric types.")
        return BoolConstraint(lambda x: lower <= x <= upper, self)

    def is_of_type(self, obj):
        return isinstance(obj, self.type)

    def bool_constraint(self, constraint: Callable[[T], bool]):
        from newDSL.constraint.BoolConstraint import BoolConstraint
        return BoolConstraint(constraint, self)

    def bool_comparator(self, comparator: Callable[[T, T, T], T]):
        from newDSL.constraint.BoolComparator import BoolComparator
        return BoolComparator(self, comparator)

    def create_metadata_value(self, value):
        if not isinstance(value, self.type):
            raise TypeError(f"Value {value} is not of type {self.type.__name__}")
        from newDSL.metadata.MetadataValue import MetadataValue
        return MetadataValue(self, value)

    @staticmethod
    def of(name: str, type_: Type[T]):
        return Metadata(name, type_)

    @staticmethod
    def of_string(name: str):
        return Metadata(name, str)

    @staticmethod
    def of_integer(name: str):
        return Metadata(name, int)

    @staticmethod
    def of_boolean(name: str):
        return Metadata(name, bool)

    @staticmethod
    def of_double(name: str):
        return Metadata(name, float)

    @staticmethod
    def of_float(name: str):
        return Metadata(name, float)

    @staticmethod
    def of_long(name: str):
        return Metadata(name, int)

    @staticmethod
    def of_character(name: str):
        return Metadata(name, str)

    @staticmethod
    def of_byte(name: str):
        return Metadata(name, bytes)

    @staticmethod
    def of_short(name: str):
        return Metadata(name, int)
