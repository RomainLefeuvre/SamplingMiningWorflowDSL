from collections.abc import Callable
from typing import List, TypeVar


T = TypeVar("T")


class Metadata[T]:
    def __init__(self, name: str, type_: type[T]):
        self.name = name
        self.type = type_

    def __hash__(self):
        return hash((self.name, self.type))

    def __eq__(self, other):
        if not isinstance(other, Metadata):
            return False
        return self.name == other.name and self.type == other.type

    def is_of_type(self, obj):
        return isinstance(obj, self.type)

    def bool_constraint(self, constraint: Callable[[T], bool]):
        from sampling_workflow.constraint.BoolConstraint import BoolConstraint

        return BoolConstraint(constraint, self)

    def bool_comparator(self, comparator: Callable[[T, T], T]):
        from sampling_workflow.constraint.BoolComparator import BoolComparator

        return BoolComparator(self, comparator)

    def create_metadata_value(self, value):
        typed_value=value
        if not isinstance(value, self.type):
            try:
                typed_value=self.type(value) #instantiate the type to convert it
            except Exception as e:
                raise TypeError(f"Value {value} is not of type {self.type} and cannot be converted to it.",e) from e
        from sampling_workflow.metadata.MetadataValue import MetadataValue

        return MetadataValue(self, typed_value)

    @staticmethod
    def of(name: str, type_: type[T]):
        return Metadata(name, type_)
    
    @staticmethod
    def of_date(name: str):
        from sampling_workflow.metadata.MetadataDate import MetadataDate

        return MetadataDate(name)

    @staticmethod
    def of_string(name: str):
        from sampling_workflow.metadata.MetadataString import MetadataString

        return MetadataString(name)

    @staticmethod
    def of_integer(name: str):
        from sampling_workflow.metadata.MetadataNumber import MetadataNumber

        return MetadataNumber(name, int)

    @staticmethod
    def of_double(name: str):
        from sampling_workflow.metadata.MetadataNumber import MetadataNumber

        return MetadataNumber(name, float)

    @staticmethod
    def of_float(name: str):
        from sampling_workflow.metadata.MetadataNumber import MetadataNumber

        return MetadataNumber(name, float)

    @staticmethod
    def of_long(name: str):
        from sampling_workflow.metadata.MetadataNumber import MetadataNumber

        return MetadataNumber(name, int)

    @staticmethod
    def of_character(name: str):
        from sampling_workflow.metadata.MetadataString import MetadataString

        return MetadataString(name)

    @staticmethod
    def of_short(name: str):
        from sampling_workflow.metadata.MetadataNumber import MetadataNumber

        return MetadataNumber(name, int)

    @staticmethod
    def of_boolean(name: str):
        from sampling_workflow.metadata.MetadataBoolean import MetadataBoolean

        return MetadataBoolean(name)

    @staticmethod
    def of_byte(name: str):
        return Metadata(name, bytes)
    
    @staticmethod
    def of_list(name: str, type,transfo:Callable[[str],List[T]]=None):
        from sampling_workflow.metadata.MetadataList import MetadataList

        return MetadataList(name,type,transfo)
