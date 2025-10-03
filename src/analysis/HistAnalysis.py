import os
from collections import Counter
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd

from src.element.Set import Set
from src.metadata.Metadata import Metadata

if TYPE_CHECKING:
    from src.metadata import MetadataValue


class HistAnalysis:
    def __init__(
        self,
        save_path: str,
        metadata: Metadata,
        top_x: int = -1,
        category: bool = True,
        sort: bool = False,
    ):
        self.metadata = metadata
        # Wether data should be treated as categorical data or continous
        self.category = category
        self.top_x = top_x
        self.sort = sort
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def analyze(self, s: Set, file_name: str, op_info: str):
        # From Set to List of Metadata values
        try:
            metadata_values = []
            for element in s.get_elements():
                if not isinstance(element, Set):
                    metadata_value: MetadataValue = element.get_metadata_value(
                        self.metadata
                    )
                    if self.metadata.type is list:
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
        except Exception as e:
            print(f"Error analyzing {self.metadata.name}: {e}")
            return

    def create_histogram(self, data: list, op_info: str):
        df = pd.DataFrame(data, columns=["value"])
        series = df["value"]

        unique_values = series.nunique()

        fig, ax = plt.subplots()
        if not self.category:
            ax.hist(x=data, bins=min(10, unique_values))
        else:
            if self.sort:
                value_counts = series.value_counts(ascending=False, sort=True)
            else:
                value_counts = series.value_counts().sort_index(ascending=True)
            value_counts.plot(kind="bar", ax=ax)
            ax.set_xlabel("Category")

        ax.set_title(op_info)
        ax.set_ylabel("Frequency")
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
