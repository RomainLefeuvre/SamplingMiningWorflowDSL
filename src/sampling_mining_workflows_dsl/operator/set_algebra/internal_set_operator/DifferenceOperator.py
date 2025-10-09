from typing import TypeVar

from sampling_mining_workflows_dsl.element.Repository import Repository
from sampling_mining_workflows_dsl.element.Set import Set
from sampling_mining_workflows_dsl.operator.Operator import Operator
from sampling_mining_workflows_dsl.operator.selection.sampling.SamplingOperator import (
    SamplingOperator,
)
from sampling_mining_workflows_dsl.operator.set_algebra.InternalSetOperator import InternalSetOperator

T = TypeVar("T")


class DifferenceOperator(InternalSetOperator):
        def __init__(self, workflow,indexes=[-1]):
            super().__init__(workflow)
            self.set_function = Set.difference      
