from abc import ABC

from sampling_workflow.operator.selection.SelectionOperator import SelectionOperator


class SamplingOperator(SelectionOperator):
    def __init__(self, workflow, cardinality: int):
        super().__init__(workflow)
        self._cardinality = cardinality
