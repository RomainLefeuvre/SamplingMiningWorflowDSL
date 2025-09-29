from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory
from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WritterFactory import WritterFactory

# P3: A Dataset of Partial Program Fixes
# DOI : 10.1145/3643991.3644889

# *Filter C projects
# *Sort desc by stars
# *Collect all closed issues

filter_operator = OperatorFactory.filter_operator
systematic_selection_operator = OperatorFactory.systematic_selection_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    language = Metadata.of_string("language")
    nb_stars = Metadata.of_integer("nbStars")
    issues = Metadata.of_string("issues")

    cardinality = 42  # Ambiguous, should be the number of projects to sample ?

    op = (
        filter_operator(language.bool_constraint(lambda x: x == "C"))
        .chain(systematic_selection_operator(cardinality, nb_stars, 1))
        .input(json_loader("input.json", nb_stars))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
