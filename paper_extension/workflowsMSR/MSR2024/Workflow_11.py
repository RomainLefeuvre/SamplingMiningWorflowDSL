from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# Greenlight: Highlighting TensorFlow APIs Energy Footprint
# DOI : 10.1145/3643991.3644894

# *Filter to keep repos with >= 100 stars
# *Filter repos with "tenserflow" in the title or owner name
# *Exclude repos with no update since Sept 2019
# *Exclude repos without declared required dependencies

filter_operator = OperatorFactory.filter_operator
interactive_manual_sampling_operator = (
    OperatorFactory.interactive_manual_sampling_operator
)

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    # Last update = last commit ?
    # manual check to ensure project has declared dependencies ?

    nb_stars = Metadata.of_integer("nbStars")
    title = Metadata.of_string("title")
    owner = Metadata.of_string("owner")
    last_commit = Metadata.of_string("lastCommit")

    op = (
        filter_operator(nb_stars.bool_constraint(lambda x: x >= 100))
        .chain(filter_operator(title.bool_constraint(lambda x: "tensorflow" in x)))
        .chain(filter_operator(owner.bool_constraint(lambda x: "tensorflow" in x)))
        .chain(filter_operator(last_commit.bool_constraint(lambda x: x > "2019-09-01")))
        .chain(interactive_manual_sampling_operator())
        .input(json_loader("input.json", nb_stars, title, owner, last_commit))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
