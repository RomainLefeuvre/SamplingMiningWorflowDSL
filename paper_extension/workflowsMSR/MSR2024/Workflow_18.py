from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# A Dataset of Microservices-based Open-Source Projects
# DOI : 10.1145/3643991.3644890

# * Filter repos with >= 1 commit in past 2 years (2021-2022)
# * Filter repos with >= 100 total commits
# * Filter repos with >= 3 contributors


# Second workflow :
# * Filter repos that have Docker-Compose file


filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    last_commit = Metadata.of_string("lastCommit")
    nb_commits = Metadata.of_integer("nbCommits")
    nb_contributors = Metadata.of_integer("nbContributors")

    op = (
        filter_operator(
            last_commit.bool_constraint(lambda x: "2021-01-01" < x < "2023-12-31")
        )
        .chain(filter_operator(nb_commits.bool_constraint(lambda x: x >= 100)))
        .chain(filter_operator(nb_contributors.bool_constraint(lambda x: x >= 3)))
        .input(json_loader("input.json", last_commit, nb_commits, nb_contributors))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
