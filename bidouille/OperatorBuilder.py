from bidouille.FilterOperator import FilterOperator
from bidouille.Builder import Builder


class OperatorBuilder(Builder):

    def __init__(self) -> None:
        self.operators = []

    @property
    def operator(self):
        return self.operators

    def add_operator(self, operator):
        self.operators.append(operator)

    def filterOperator(self, constraint) -> Builder:
        filterOperator = FilterOperator(constraint)
        self.add_operator(filterOperator)
        return self

    def build(self):
        return self.operators