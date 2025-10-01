
from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# On the Effectiveness of Machine Learning-based Call Graph Pruning: An Empirical Study
# DOI : 10.1145/3643991.3644897

# * Filter for repos with > 80% test coverage
# * Select 40 projects (randomly ?)

filter_operator = OperatorFactory.filter_operator
random_selection_operator = OperatorFactory.random_selection_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    test_coverage = Metadata.of_float("testCoverage")

    op = (
        filter_operator(test_coverage.bool_constraint(lambda x: x > 0.8))
        .chain(random_selection_operator(40, seed=42))
        .input(json_loader("input.json", test_coverage))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
