from newDSL2.constraint.Constraint import Constraint
from newDSL2.operator.Operator import Operator
from newDSL2.element.Set import Set

class FilterOperator(Operator):
    def __init__(self, constraint: Constraint):
        super().__init__()
        self._constraint = constraint


    def execute(self):
        self._output = Set()
        for element in self._input.get_elements():
            if self._constraint.is_satisfied(element):
                self._output.add_element(element)
        super().execute()
        return self