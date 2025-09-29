from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# Keep Me Updated: An Empirical Study on Embedded JavaScript Engines in Android Apps
# DOI : 10.1145/3643991.3644901


# *Filter repos with vuln identifiers in readme files
# *Filter JS repos

filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    has_vuln_identifier = Metadata.of_boolean("hasVulnerabilityIdentifier")
    language = Metadata.of_string("language")

    op = (
        filter_operator(has_vuln_identifier.bool_constraint(lambda x: x))
        .chain(filter_operator(language.bool_constraint(lambda x: x == "JavaScript")))
        .input(json_loader("input.json", has_vuln_identifier, language))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
