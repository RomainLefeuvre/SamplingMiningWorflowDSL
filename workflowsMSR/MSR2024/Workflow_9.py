from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# On the Executability of R Markdown Files
# DOI : 10.1145/3643991.3644931

# *Filter project with primary language R
# *Exclude forked and and deleted projects
#
# *Search for R Markdown files
# *Exclude projects without any R Markdown files


filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    language = Metadata.of_string("language")
    is_forked = Metadata.of_integer("is_forked")
    is_deleted = Metadata.of_integer("is_deleted")
    has_markdown_file = Metadata.of_integer("has_markdown_file")

    op = (
        filter_operator(language.bool_constraint(lambda x: x == "R"))
        .chain(filter_operator(is_forked.bool_constraint(lambda x: not x)))
        .chain(filter_operator(is_deleted.bool_constraint(lambda x: not x)))
        .chain(filter_operator(has_markdown_file.bool_constraint(lambda x: x)))
        .input(
            json_loader(
                "GHTorrent.json", language, is_forked, is_deleted, has_markdown_file
            )
        )
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
