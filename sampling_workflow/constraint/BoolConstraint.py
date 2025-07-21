from typing import Callable, Tuple, TypeVar, Optional
from sampling_workflow.Workflow import Workflow
from sampling_workflow.constraint.Constraint import Constraint
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.element.Element import Element

T = TypeVar('T')

class BoolConstraint(Constraint[T]):
    def __init__(self, workflow,constraint: Callable[Tuple[T, ...], bool] , *targeted_metadatas: Tuple[Metadata[T],...]):
        super().__init__(workflow,*targeted_metadatas)
        self.constraint = constraint
        self.or_constraint: Optional[Constraint] = None
        self.and_constraint: Optional[Constraint] = None

    def is_satisfied(self, element: Element) -> bool:
        if self.or_constraint is not None and self.and_constraint is not None:
            raise RuntimeError("Both 'and' & 'or' constraints are defined")

        value_objs = [element.get_metadata_value(target_metadata).get_value() for target_metadata in self.targeted_metadatas ]
        # TODO add type check
        # if not isinstance(value_objs, self.targeted_metadatas.type):
        #     raise RuntimeError(f"Unexpected metadata type: {type(value_objs)}")

        
        constraint_result = self.constraint(*value_objs)

        if self.or_constraint is not None:
            return constraint_result or self.or_constraint.is_satisfied(element)
        if self.and_constraint is not None:
            return constraint_result and self.and_constraint.is_satisfied(element)

        return constraint_result

    def or_(self, other: 'BoolConstraint') -> 'BoolConstraint':
        self.or_constraint = other
        return other

    def and_(self, other: 'BoolConstraint') -> 'BoolConstraint':
        self.and_constraint = other
        return other