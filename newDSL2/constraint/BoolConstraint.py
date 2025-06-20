from typing import Callable, TypeVar, Optional
from newDSL.constraint.Constraint import Constraint
from newDSL.metadata.Metadata import Metadata
from newDSL.element.Element import Element

T = TypeVar('T')

class BoolConstraint(Constraint[T]):
    def __init__(self, constraint: Optional[Callable[[T], bool]] = None, targeted_metadata: Optional[Metadata[T]] = None):
        super().__init__(targeted_metadata)
        self.constraint = constraint
        self.or_constraint: Optional[Constraint] = None
        self.and_constraint: Optional[Constraint] = None

    def is_satisfied(self, element: Element) -> bool:
        if self.or_constraint is not None and self.and_constraint is not None:
            raise RuntimeError("Both 'and' & 'or' constraints are defined")

        value_obj = element.get_metadata_value(self.targeted_metadata).get_value()
        if not isinstance(value_obj, self.targeted_metadata.type):
            raise RuntimeError(f"Unexpected metadata type: {type(value_obj)}")

        value: T = value_obj
        constraint_result = self.constraint(value)

        if self.or_constraint is not None:
            return constraint_result or self.or_constraint.is_satisfied(element)
        if self.and_constraint is not None:
            return constraint_result and self.and_constraint.is_satisfied(element)

        return constraint_result

    def or_constraint(self, other: 'BoolConstraint') -> 'BoolConstraint':
        self.or_constraint = other
        return other

    def and_constraint(self, other: 'BoolConstraint') -> 'BoolConstraint':
        self.and_constraint = other
        return other