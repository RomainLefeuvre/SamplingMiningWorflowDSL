from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# Incivility in Open Source Projects: A Comprehensive Annotated Dataset of Locked GitHub Issue Threads
# DOI : 10.1145/3643991.3644887

# * Filter projects with >= 50 contributors

filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    nb_contributors = Metadata.of_integer("nbContributors")

    op = (
        filter_operator(nb_contributors.bool_constraint(lambda x: x >= 50))
        .input(json_loader("input.json"))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
