from typing import Any


class Sandwich:

    def __init__(self) -> None:
        self._parts = []

    def add(self, part: Any) -> None:
        self._parts.append(part)
        