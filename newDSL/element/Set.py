import random
from typing import List, Iterator
from newDSL.element.Element import Element

class Set(Element):
    def __init__(self):
        super().__init__()
        self.elements = []

    def add_element(self, element: Element) -> 'Set':
        self.elements.append(element)
        return self

    def union(self, other: 'Set') -> 'Set':
        self.elements.append(other.elements)
        return self

    def set_elements(self, elements: set) -> None:
        self.elements = elements

    def get_random_subset(self, subset_size: int, seed: int) -> 'Set':
        if subset_size > len(self.elements):
            print(f"Caution, subset size is larger than the size of the original set, subset size: {subset_size}, current set size: {len(self.elements)}")
            subset_size = len(self.elements)

        random.seed(seed)
        random_indices = random.sample(range(len(self.elements)), subset_size)
        original_array = list(self.elements)

        result = Set()
        for index in random_indices:
            result.add_element(original_array[index])

        return result

    def get_elements(self) -> List[Element]:
        return list(self.elements)

    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, level: int) -> str:
        truncate_after = 10
        indent = "    " * level

        result = f"{indent}(size={len(self.elements)})["
        it: Iterator[Element] = iter(self.elements)
        element_to_print = min(truncate_after, len(self.elements))

        for i in range(element_to_print):
            next_element = next(it)
            if isinstance(next_element, Set):
                result += f"\n{next_element.to_string(level + 4)}"
            else:
                result += str(next_element)

            if i != element_to_print - 1:
                result += ","

        if len(self.elements) > truncate_after:
            result += "...]"
        else:
            result += "]"

        return result