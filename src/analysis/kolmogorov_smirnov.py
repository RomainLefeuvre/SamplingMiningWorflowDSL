
from scipy.stats import ks_2samp

from src.element.Repository import Repository
from src.element.Set import Set
from src.metadata.Metadata import Metadata


class kolmogorov_smirnov:
    def __init__(self, metadata: Metadata[int]):
        self.metadata = metadata

    def analyze(self, a: Set, sample: Set) -> float:
        first_list = self.extract_list(a)
        second_list = self.extract_list(sample)

        # Perform the Kolmogorov-Smirnov test
        ks_stat, ks_p_value = ks_2samp(first_list, second_list)
        return ks_p_value

    def extract_list(self, s: Set) -> list[int]:
        metadata_values = []

        for element in s.get_elements():
            if isinstance(element, Repository):
                repo: Repository = element
                metadata_value = repo.get_metadata_value(self.metadata)
                if metadata_value:
                    metadata_values.append(metadata_value.get_value())

        return metadata_values
