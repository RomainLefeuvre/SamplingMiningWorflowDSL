from newDSL2.element.Repository import Repository
from newDSL2.element.Set import Set
from newDSL2.metadata.Metadata import Metadata
import matplotlib.pyplot as plt
import os

class HistAnalysis:
    def __init__(self, metadata: Metadata, save_path: str):
        self.metadata = metadata
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)  # Ensure the directory exists

    def analyze(self, s: Set, file_name: str, op_info: str):
        # From Set to List of Metadata values
        metadata_values = []
        for element in s.get_elements():
            if isinstance(element, Repository):
                metadata_values.append(element.get_metadata_value(self.metadata).get_value())

        self.save_histogram(metadata_values, file_name, op_info)

    def save_histogram(self, data: list, file_name: str, op_info: str):
        plt.hist(x=data)
        plt.title(op_info)

        file_path = os.path.join(self.save_path, file_name)

        # Save the plot
        plt.savefig(file_path)
        plt.close()  # Close the plot to free memory