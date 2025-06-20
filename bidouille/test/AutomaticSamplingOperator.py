from abc import ABC

from newDSL.operator.selection.sampling.SamplingOperator import SamplingOperator


class AutomaticSamplingOperator(SamplingOperator):
    def __init__(self, cardinality: int):
        super().__init__(cardinality)