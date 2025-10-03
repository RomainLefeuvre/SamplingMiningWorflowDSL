
from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# The PIPr Dataset of Public Infrastructure as Code Programs
# DOI : 10.1145/3643991.3644888

# * Filter repos with one IaC configuration file
# * Filter not a fork OR fork with more stars than parent
# * Filter repos with < 500 000 files
# * Filter repos with activity within last year OR returned in search results
# * Filter repos with searched files in default branch
# * Filter repos with searched files < 384 KB


filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    is_fork = Metadata.of_boolean("isFork")
    nb_stars = Metadata.of_integer("nbStars")
    parent_nb_stars = Metadata.of_integer("parentNbStars")
    nb_files = Metadata.of_integer("nbFiles")
    last_activity = Metadata.of_string("lastActivity")
    in_search_results = Metadata.of_boolean("inSearchResults")

    # Searched files ? -> IaC files ?
    searched_files_default_branch = Metadata.of_boolean("searchedFilesDefaultBranch")
    size = Metadata.of_integer("size")

    op = (
        filter_operator(
            is_fork.bool_constraint(lambda x: not x).or_(
                # bool constraint can't take 2 metadata (parent_nb_stars can't be used this way
                is_fork.bool_constraint(lambda x: x).and_(
                    nb_stars.bool_constraint(lambda x: x > parent_nb_stars)
                )
            )
        )  # or condition like this ?
        .chain(filter_operator(nb_files.bool_constraint(lambda x: x < 500000)))
        .chain(
            filter_operator(
                last_activity.bool_constraint(lambda x: x > "2023-01-01").or_(
                    in_search_results.bool_constraint(lambda x: x)
                )
            )
        )
        # .chain(filter_operator(last_activity.bool_constraint(lambda x: x > "2023-01-01"))) # Or returned in search results ?
        .chain(
            filter_operator(searched_files_default_branch.bool_constraint(lambda x: x))
        )
        .chain(
            filter_operator(size.bool_constraint(lambda x: x < 384 * 1024))
        )  # 384 KB
        .input(
            json_loader(
                "input.json",
                is_fork,
                nb_stars,
                parent_nb_stars,
                nb_files,
                last_activity,
                searched_files_default_branch,
                size,
            )
        )
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
