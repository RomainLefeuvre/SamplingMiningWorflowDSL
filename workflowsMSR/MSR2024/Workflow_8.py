from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# AW4C: A Commit-Aware C Dataset for Actionable Warning Identification
# DOI : 10.1145/3643991.3644885

# *Filter C repos
# *Sort by number of stars
# *Keep 500 top repos
# *Exclude repos with > 100K commits

filter_operator = OperatorFactory.filter_operator
systematic_selection_operator = OperatorFactory.systematic_selection_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    language = Metadata.of_string("language")
    nb_stars = Metadata.of_integer("nbStars")
    nb_commits = Metadata.of_integer("nbCommits")

    op = (
        filter_operator(language.bool_constraint(lambda x: x == "C"))
        .chain(systematic_selection_operator(500, nb_stars, 1))
        .chain(filter_operator(nb_commits.bool_constraint(lambda x: x > 100000)))
        .input(json_loader("input.json", language, nb_stars, nb_commits))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
