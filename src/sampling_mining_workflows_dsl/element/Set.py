import random
from functools import cmp_to_key
from collections import OrderedDict

from sampling_mining_workflows_dsl.constraint.Comparator import Comparator
from sampling_mining_workflows_dsl.element.Element import Element


class Set(Element):
    def __init__(self):
        super().__init__()
        self.elements = OrderedDict()
        self.ids= set()

    def __hash__(self):
        return hash(tuple(self.elements.items)) + super().__hash__()

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not isinstance(other, Set):
            return False
        return self.elements == other.elements
    
    def get_element_by_index(self, index: int) -> Element:
        if index < 0 or index >= len(self.elements):
            raise IndexError("Index out of range")
        return list(self.elements.values())[index]
    
    def add_element(self, element: Element) -> "Set":
        if not element.get_id() in self.ids:
            self.elements[element.get_id()]=element
            self.ids.add(element.get_id())
        else :
            print(f"{element.get_id()} Already present")

        return self

    def sort_by_metadata(self, metadata_name: str, comparator: Comparator, reverse=False) -> "Set":
        # Sort the items of the OrderedDict
        sorted_items = sorted(
            self.elements.items(),
            key=cmp_to_key(lambda x, y: comparator.compare(x[1], y[1])),
            reverse=reverse
        )
    
        # Rebuild as OrderedDict
        self.elements = OrderedDict(sorted_items)
        return self

    def get_depth(self) -> int:
        max_depth = 1
        for element in self.elements.values():
            if isinstance(element, Set):
                max_depth = max(max_depth, 1 + element.get_depth())
        return max_depth
    
    def union(self, other: "Set") -> "Set":
        for element in other.elements.values():
            self.add_element(element)
        return self
    
    def intersection(self, other: "Set") -> "Set":
        common_elements = Set()
        for id, element in self.elements.items():
            if id in other.elements.keys():
                common_elements.add_element(element)
        return common_elements
    
    def difference(self, other: "Set") -> "Set":
        """Return a new set with elements in this set but not in other"""
        diff_elements = Set()
        for id, element in self.elements.items():
            if id not in other.elements.keys():
                diff_elements.add_element(element)
        return diff_elements
    
    def symmetric_difference(self, other: "Set") -> "Set":
        """Return a new set with elements in either set but not in both"""
        sym_diff = Set()
        
        # Add elements from this set that are not in other
        for id, element in self.elements.items():
            if id not in other.elements.keys():
                sym_diff.add_element(element)
        
        # Add elements from other set that are not in this
        for id, element in other.elements.items():
            if id not in self.elements.keys():
                sym_diff.add_element(element)
        
        return sym_diff
    
    def is_subset(self, other: "Set") -> bool:
        """Return True if all elements in this set are also in other"""
        for id in self.elements.keys():
            if id not in other.elements.keys():
                return False
        return True
    
    def is_superset(self, other: "Set") -> bool:
        """Return True if all elements in other set are also in this set"""
        return other.is_subset(self)
    
    def is_disjoint(self, other: "Set") -> bool:
        """Return True if this set and other have no elements in common"""
        for id in self.elements.keys():
            if id in other.elements.keys():
                return False
        return True
    
    def is_empty(self) -> bool:
        """Return True if the set is empty"""
        return len(self.elements) == 0
    
   

    def size(self) -> int:
        return len(self.elements)

    def get_element(self, id: str) -> Element:
        if not id  in self.elements.keys():
            raise RuntimeError(f"Element with id {id} not found in the set")
        return self.elements.get(id)
    

    def get_id(self):
        set_id = ""
        for id in self.elements.keys():
            set_id = set_id + "_" + id
        return set_id

    def flatten_set(self) -> "Set":
        flattened = Set()
        for element in self.get_elements():
            if isinstance(element, Set):
                # Recursively flatten nested Sets
                flattened.union(element.flatten_set())
            else:
                # Add non-Set, non-list elements directly
                flattened.add_element(element)
        return flattened


    def get_random_subset(self, subset_size: int, seed: int) -> "Set":
        elements_list = self.get_elements()
        if subset_size > len(elements_list):
            print(
                f"Caution, subset size is larger than the size of the original set, subset size: {subset_size}, current set size: {len(elements_list)}"
            )
            subset_size = len(elements_list)

        random.seed(seed)
        random_indices = random.sample(range(len(elements_list)), subset_size)
        original_array = list(elements_list)

        result = Set()
        for index in random_indices:
            result.add_element(original_array[index])

        return result

    def get_elements(self) -> list[Element]:
        return list(self.elements.values())

    def __str__(self) -> str:
        return self.to_string(0)

    def to_string(self, level: int = 0) -> str:
        truncate_after = 10
        indent = "    " * level

        result = f"{indent}(size={len(self.elements)})["
        elements_list = self.get_elements()
        element_to_print = min(truncate_after, len(self.elements))

        for i in range(element_to_print):
            next_element = elements_list[i]

            if isinstance(next_element, Set):
                # Recursively call to_string for nested Sets
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
