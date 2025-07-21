from sampling_workflow.element.Repository import Repository
from sampling_workflow.element.Set import Set
from sampling_workflow.metadata import MetadataValue
from sampling_workflow.metadata.Metadata import Metadata
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter

class HistAnalysis:
    def __init__(self, metadata: Metadata,top_x: int = -1):
        self.metadata = metadata
        self.top_x = top_x

    def analyze(self, s: Set, op_info: str):
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


        self.show_histogram(metadata_values, op_info)

    def show_histogram(self, data: list, op_info: str,sort=False, bins=10, unique_threshold=20):
        df = pd.DataFrame(data, columns=['value'])
        series = df['value']

        # Determine if the data is categorical or continuous
        is_numeric = pd.api.types.is_numeric_dtype(series)
        unique_values = series.nunique()

        if is_numeric and unique_values > unique_threshold:
            # Continuous data: use histogram or binning
            df['binned'] = pd.cut(series, bins=bins)
            value_counts = df['binned'].value_counts().sort_index()
            value_counts.plot(kind='bar')
            plt.xlabel('Bins')
        else:
            # Categorical or discrete numeric
            if sort:
                value_counts = series.value_counts().sort_index(  ascending=False)
            else:
                value_counts = series.value_counts()
            value_counts.plot(kind='bar')
            plt.xlabel('Category')

        plt.title(op_info)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()

