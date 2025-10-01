from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# Multi-faceted Code Smell Detection at Scale using DesigniteJava 2.0
# DOI : 10.1145/3643991.3644881

# *Filter Java repositories
# *Filter for projects with size between 10K and 15K
# *Filter for projects with unit-test
# *Filter for projects with documentation > 0.0
# *Filter for projects with >= 2 developpers
# *Sort by number of stars
#
# *Purposive sampling to keep only one repo

filter_operator = OperatorFactory.filter_operator
interactive_manual_sampling_operator = (
    OperatorFactory.interactive_manual_sampling_operator
)
systematic_selection_operator = OperatorFactory.systematic_selection_operator


json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    # Take top 3 when sorted by stars, and then purpose sampling ?

    language = Metadata.of_string("language")
    size = Metadata.of_integer("size")
    has_unit_test = Metadata.of_boolean("hasUnitTest")
    documentation_ratio = Metadata.of_float("documentationRatio")
    nb_developpers = Metadata.of_integer("nbDeveloppers")
    nb_stars = Metadata.of_integer("nbStars")

    op = (
        filter_operator(language.bool_constraint(lambda x: x == "Java"))
        .chain(filter_operator(size.bool_constraint(lambda x: 10000 <= x <= 15000)))
        .chain(filter_operator(has_unit_test.bool_constraint(lambda x: x)))
        .chain(filter_operator(documentation_ratio.bool_constraint(lambda x: x > 0.0)))
        .chain(filter_operator(nb_developpers.bool_constraint(lambda x: x >= 2)))
        .chain(systematic_selection_operator(3, nb_stars, 1))
        .chain(interactive_manual_sampling_operator())
        .input(
            json_loader(
                "RepoReapers.json",
                language,
                size,
                has_unit_test,
                documentation_ratio,
                nb_developpers,
                nb_stars,
            )
        )
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
