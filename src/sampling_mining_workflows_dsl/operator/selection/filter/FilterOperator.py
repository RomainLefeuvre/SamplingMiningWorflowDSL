from sampling_mining_workflows_dsl.constraint.Constraint import Constraint
from sampling_mining_workflows_dsl.element.Set import Set
from sampling_mining_workflows_dsl.operator.Operator import Operator


class FilterOperator(Operator):
    def __init__(self, workflow, constraint: Constraint):
        super().__init__(workflow)
        self._constraint = constraint
        constraint.set_workflow(workflow)

    def execute(self):
        self._output = Set()
        for element in self._input.get_elements():
            if self._constraint.is_satisfied(element):
                self._output.add_element(element)
        super().execute()
        return self

    def get_constraint(self) -> Constraint:
        return self._constraint
