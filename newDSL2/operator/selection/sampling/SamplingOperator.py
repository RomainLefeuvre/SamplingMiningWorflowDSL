from abc import ABC

from newDSL2.operator.selection.SelectionOperator import SelectionOperator


class SamplingOperator(SelectionOperator):
    def __init__(self, cardinality: int):
        super().__init__()
        self._cardinality = cardinality