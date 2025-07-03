from newDSL2.element.Repository import Repository
from newDSL2.element.Set import Set
from newDSL2.metadata.Metadata import Metadata
import matplotlib.pyplot as plt
import numpy as np

class HistAnalysis:
    def __init__(self, metadata: Metadata):
        self.metadata = metadata

    def analyze(self, s: Set, op_info: str):
        # From Set to List of Metadata values
        metadata_values = []
        for element in s.get_elements():
            if isinstance(element, Repository):
                metadata_values.append(element.get_metadata_value(self.metadata).get_value())

        self.show_histogram(metadata_values, op_info)

    def show_histogram(self, data: list, op_info: str):
        plt.hist(x=data)
        plt.title(op_info)
        plt.show()