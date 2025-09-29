from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# BugsPHP: A dataset for Automated Program Repair in PHP
# DOI : 10.1145/3643991.3644878

# *Filter PHP projects
# *Sort by number of stars and latest commit date
# *Filter when >= 1 commit date after 1st Jan 2021
# *Keep top 5,000 repos
#
# *Collect commits


filter_operator = OperatorFactory.filter_operator
systematic_selection_operator = OperatorFactory.systematic_selection_operator


json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    language = Metadata.of_string("language")
    nb_stars = Metadata.of_integer("nbStars")
    last_commit_date = Metadata.of_string("lastCommitDate")

    op = (
        filter_operator(language.bool_constraint(lambda x: x == "PHP"))
        .chain(
            filter_operator(
                last_commit_date.bool_constraint(lambda x: x > "2021-01-01")
            )
        )
        # Sorted by number of stars and then latest commit date ?
        .chain(systematic_selection_operator(5000, nb_stars, 1))
        .chain(systematic_selection_operator(5000, last_commit_date, 1))
        .input(json_loader("input.json", language, nb_stars, last_commit_date))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
