from bidouille.Operator import Operator

class FilterOperator(Operator):
    def __init__(self, constraint) -> None:
        super().__init__()
        self._attr = 0