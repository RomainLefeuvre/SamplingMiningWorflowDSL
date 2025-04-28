from typing import List

from newDSL.element.Set import Set
from newDSL.operator.Operator import Operator


class GroupingOperator(Operator):
    def __init__(self, *operators: Operator):
        super().__init__()
        self.operators: List[Operator] = list(operators)
        for operator in self.operators:
            operator.input_set(self._input)

    def execute(self) -> Operator:
        self._output = Set()
        for selection_operator in self.operators:
            selection_operator.input_set(self._input)
            selection_operator.execute_workflow()
            self._output.union(selection_operator.get_output())

        super().execute()
        return self

    def get_operators(self) -> List[Operator]:
        return self.operators

    def extra_to_string(self, level: int) -> str:
        indent = "    " * (level + 1)
        res = f"\n{indent}Internal Operators:"
        for selection_operator in self.operators:
            res += f"\n{selection_operator.to_string(level + 1)}"
        return res