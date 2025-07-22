import os

from sampling_workflow.element.Repository import Repository
from sampling_workflow.element.Set import Set
from sampling_workflow.metadata import MetadataValue
from sampling_workflow.metadata.Metadata import Metadata
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter

class HistAnalysis:
    def __init__(self, save_path: str, metadata: Metadata,top_x: int = -1, sort: bool = False):
        self.metadata = metadata
        self.top_x = top_x
        self.sort = sort
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def analyze(self, s: Set, file_name: str, op_info: str):
        # From Set to List of Metadata values
        metadata_values = []
        for element in s.get_elements():
            if not isinstance(element, Set):
                metadata_value: MetadataValue = element.get_metadata_value(self.metadata)
                if self.metadata.type == list:
                    metadata_values.extend(metadata_value.get_value())
                else:
                    metadata_values.append(metadata_value.get_value())

        if self.top_x > 0:
            # Count all and find top_x
            counter = Counter(metadata_values)
            most_common = dict(counter.most_common(self.top_x))
            top_values = set(most_common.keys())

            # Replace non-top values with 'Other'
            metadata_values = [
                val if val in top_values else "Other" for val in metadata_values
            ]

        fig, ax = self.create_histogram(metadata_values, op_info)
        self.show_histogram()
        self.save_histogram(fig, file_name)

    def create_histogram(self, data: list, op_info: str, bins=10, unique_threshold=5):
        df = pd.DataFrame(data, columns=['value'])
        series = df['value']

        is_numeric = pd.api.types.is_numeric_dtype(series)
        unique_values = series.nunique()

        fig, ax = plt.subplots()
        if is_numeric and unique_values > unique_threshold:
            ax.hist(x=data, bins=bins)
        else:
            if self.sort:
                value_counts = series.value_counts().sort_index(ascending=False)
            else:
                value_counts = series.value_counts()
            value_counts.plot(kind='bar', ax=ax)
            ax.set_xlabel('Category')

        ax.set_title(op_info)
        ax.set_ylabel('Frequency')
        plt.tight_layout()
        return fig, ax

    def save_histogram(self, fig, file_name: str):
        if file_name:
            file_path = os.path.join(self.save_path, file_name)
            fig.savefig(file_path)
        else:
            print("No save path provided, displaying histogram instead.")
            self.show_histogram()
        plt.close(fig)


    def show_histogram(self):
        plt.show()

