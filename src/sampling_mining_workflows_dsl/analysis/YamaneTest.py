import math


class YamaneTest:
    def __init__(self, population_size: int, margin_of_error: float):
        self.population_size = population_size
        self.margin_of_error = margin_of_error

    def calculate_required_sample_size(self) -> int:
        return math.ceil(
            self.population_size / (1 + self.population_size * self.margin_of_error**2)
        )

    def is_representative(self, given_sample_size: int) -> bool:
        required_sample_size = self.calculate_required_sample_size()
        return given_sample_size >= required_sample_size
