from abc import ABC

from sampling_workflow.operator.selection.sampling.SamplingOperator import (
    SamplingOperator,
)


class AutomaticSamplingOperator(SamplingOperator):
    def __init__(self, workflow, cardinality: int):
        super().__init__(workflow, cardinality)
