from typing import Optional
from bidouille.test.Element import Element

class Operator:
    def __init__(self):
        self._input: Optional[Element] = None
        self._output: Optional[Element] = None
        self._next_operator: Optional["Operator"] = None
        self._previous_operator: Optional["Operator"] = None

    def __str__(self):
        return self.__class__.__name__
