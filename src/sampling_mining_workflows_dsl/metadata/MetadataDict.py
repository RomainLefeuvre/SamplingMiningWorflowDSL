from collections.abc import Callable
from typing import TypeVar

from sampling_mining_workflows_dsl.metadata.Metadata import Metadata

K, V = TypeVar("K"), TypeVar("V")

class MetadataDict(Metadata[dict[K, V]]):
    transfo : Callable[[str],dict[K, V]]

    def __init__(self, name: str, key_type: type[K], value_type: type[V], transfo:Callable[[str],dict[K, V]]=None):
        self.full_type=dict[key_type, value_type]
        self.transfo=transfo
        super().__init__(name,dict)

    def create_metadata_value(self, value):
        #Check if value is a dict of K,V
        result=value
        if not self.checkType(result):
            result=self.transfo(result)

        if not self.checkType(result):
            raise TypeError(f"Value {value} is not of type {self.full_type}")
        return super().create_metadata_value(result)

    def addTransformation(self,transfo:Callable[[str],dict[K, V]]):
        self.transfo=transfo
        return self

    def checkType(self,obj):
        if not isinstance(obj,dict):
            return False
        return all(isinstance(key, self.full_type.__args__[0]) and isinstance(value, self.full_type.__args__[1]) for key, value in obj.items())
