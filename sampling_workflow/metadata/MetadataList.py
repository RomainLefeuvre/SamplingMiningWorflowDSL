from collections.abc import Callable
from typing import List
from sampling_workflow.metadata.Metadata import Metadata

from typing import TypeVar, Generic, List

T = TypeVar("T")
class MetadataList(Metadata[List[T]]):
    transfo : Callable[[str],List[T]]

    def __init__(self, name: str,type,transfo:Callable[[str],List[T]]=None):
        self.full_type=type
        self.transfo=transfo
        super().__init__(name,list)

    def create_metadata_value(self, value):
                #Check if value is a List of string of T
                result=value
                if not self.checkType(result):
                     result=self.transfo(result)

                if not self.checkType(result):
                    raise TypeError(f"Value {value} is not of type {self.full_type}")
                return super().create_metadata_value(result)

    def addTransformation(self,transfo:Callable[[str],List[T]]):
        self.transfo=transfo
        return self
    
    def checkType(self,obj):
        if not isinstance(obj,list):
            return False
        for item in obj:
            if not isinstance(item,self.full_type.__args__[0]):
                return False
        return True
