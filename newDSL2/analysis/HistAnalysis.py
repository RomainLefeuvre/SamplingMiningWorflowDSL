from newDSL2.element.Repository import Repository
from newDSL2.element.Set import Set
from newDSL2.metadata.Metadata import Metadata
import matplotlib.pyplot as plt
import numpy as np

class HistAnalysis:
    def __init__(self, metadata: Metadata):
        self.metadata = metadata

    def analyze(self, s: Set):
        # From Set to List of Metadata values
        metadata_values = []
        for element in s.get_elements():
            if isinstance(element, Repository):
                metadata_values.append(element.get_metadata_value(self.metadata).get_value())

        self.show_histogram(metadata_values)

    def show_histogram(self, data: list):
        plt.hist(data)
        plt.show()