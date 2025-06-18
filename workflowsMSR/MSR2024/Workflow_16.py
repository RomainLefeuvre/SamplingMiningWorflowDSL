from newDSL.metadata.Metadata import Metadata
from newDSL.operator.OperatorFactory import OperatorFactory
from newDSL.element.loader.LoaderFactory import LoaderFactory
from newDSL.element.writer.WritterFactory import WritterFactory

# "Opening the Valve on Pure-Data: Usage Patterns and Programming Practices of a Data-Flow Based Visual Programming Language"
# DOI : 1145/3643991.3644865

# * Retrieve GitHub repos based on list of project names
# * Filter repos with PD files (manually or GitHub API ?)
# * Filter for public projects (obvious ig ?)

filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

def main():

    has_pd_files = Metadata.of_boolean("hasPDFiles")

    op = (
        # * Retrieve GitHub repos based on list of project names
        filter_operator(has_pd_files.bool_constraint(lambda x: x))
        .input(json_loader("input.json", has_pd_files))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)