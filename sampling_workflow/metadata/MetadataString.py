from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.constraint.BoolConstraint import BoolConstraint

class MetadataString(Metadata[str]):
    def __init__(self, name: str):
        super().__init__(name, str)

    def is_equal(self, value: str) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x == value, self)
    
    def is_not_equal(self, value: str) -> BoolConstraint:
        return BoolConstraint(None, lambda x: x!= value, self)