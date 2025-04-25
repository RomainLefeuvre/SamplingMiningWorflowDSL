from sandwich.Builder import Builder
from sandwich.Sandwich import Sandwich


class SandwichBuilder(Builder):

    def __init__(self) -> None:
        self._sandwich = Sandwich()

    @property
    def sandwich(self) -> Sandwich:
        return self._sandwich

    def reset(self) -> None:
        self._sandwich = Sandwich()

    def addTomato(self) -> Builder:
        self._sandwich.add("Tomato")
        return self

    def addLettuce(self) -> Builder:
        self._sandwich.add("Lettuce")
        return self

    def addMeat(self) -> Builder:
        self._sandwich.add("Meat")
        return self

    def addBread(self) -> Builder:
        self._sandwich.add("Bread")
        return self

