from bidouille.test.Operator import Operator

class SampleOperator(Operator):
    def __init__(self, cardinality: int):
        super().__init__()
        self.cardinality = cardinality

    def __str__(self):
        return f"SampleOperator(cardinality={self.cardinality})"