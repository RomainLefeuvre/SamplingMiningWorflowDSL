# Enhancing Performance Bug Prediction Using Performance Code Metrics
# DOI : 10.1145/3643991.3644920

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# clone projects on Github, given a list from GHTorrent
# filter to keep Java projects
# > 2,000 commits
# exclude archived and forked projects
# exclude when no bug reports
# exclude when managed by bug tracking systems (Kira, Bugzilla, ...)
# exclude when lifespan < 1 year
# exclude when have limited performance bug fixing commits
# exclude when no performance bug fixing commits in their last six months periods

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer
filter_operator = OperatorFactory.filter_operator

#Todo fix old syntax
def main():
    language = Metadata.of_string("language")
    commit_nb = Metadata.of_integer("commitNb")
    is_archived = Metadata.of_boolean("isArchived")
    is_forked = Metadata.of_boolean("isForked")
    no_bug_report = Metadata.of_boolean("noBugReport")
    is_managed_bugtracking = Metadata.of_boolean("isManagedBugTracking")

    # Or calculated lifespan ? Which unit ?
    first_commit = Metadata.of_double("firstCommit")
    last_commit = Metadata.of_double("lastCommit")
    lifespan = Metadata.of_double("lifespan")

    # Method on his own to allow this very precise filter ?
    has_limited_performance_bug_fixing_commit = Metadata.of_boolean(
        "hasLimitedPerformanceBugFixingCommit"
    )
    # Same with last criteria

    op = (
        filter_operator(language.bool_constraint(lambda x: x == "Java"))
        .chain(filter_operator(commit_nb.bool_constraint(lambda x: x >= 2000)))
        .chain(filter_operator(is_archived.bool_constraint(lambda x: not x)))
        .chain(filter_operator(is_forked.bool_constraint(lambda x: not x)))
        .chain(filter_operator(no_bug_report.bool_constraint(lambda x: not x)))
        .chain(filter_operator(is_managed_bugtracking.bool_constraint(lambda x: not x)))
        .chain(filter_operator(lifespan.bool_constraint(lambda x: x > 1)))
        .chain(
            filter_operator(
                has_limited_performance_bug_fixing_commit.bool_constraint(
                    lambda x: not x
                )
            )
        )
        .input(
            json_loader(
                "GHTorrent.json",
                language,
                commit_nb,
                is_archived,
                is_forked,
                has_limited_performance_bug_fixing_commit,
            )
        )
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)


if __name__ == "__main__":
    main()
