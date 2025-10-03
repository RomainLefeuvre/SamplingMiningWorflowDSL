from sampling_workflow.element.Loader import Loader
from sampling_workflow.element.loader.LoaderFactory import *
from sampling_workflow.element.writer.WriterFactory import *
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# Investigating the Resolution of Vulnerable Dependencies with Dependabot Security Updates.


# * Filter project non fork
# * Filter project with more than X stars
# * Filter project with a commit before June 1,2019
# * Filter project with at least an update after June 1,2019
# *Filter project with more than 100 commits in June 1,2019
# * Filter project with at least one commit for each months between June 1,2019 and May 31,2020
# * Filter project including package.json manifest at the root
# * Filter project using Reaper
# 3151 projects
# * Filter project having at least a dependabot security update targeting npm or yarn
# * Filter out project that use multiple dependency management bots
# (Maven, RubyGem)


class CommitsMetadata:
    def get_first_commit_date(self) -> int | None:
        # placeholder: should return epoch day of first commit
        return None

    def get_number_of_commit_by_month(self, year: int, month: int) -> int | None:
        # placeholder: should return number of commits in given month
        return None

    def get_total_commit_at_date(self, day: int, month: int, year: int) -> int | None:
        # placeholder: should return total commits up to given date
        return None

    def get_total_commit(self) -> int | None:
        # placeholder: should return total commits
        return None


def months_between(start_year, start_month, end_year, end_month):
    """Generate (year, month) tuples between two inclusive dates."""
    for i in range((end_year - start_year) * 12 + (end_month - start_month) + 1):
        year = start_year + (start_month + i - 1) // 12
        month = (start_month + i - 1) % 12 + 1
        yield year, month


def main():
    url = Metadata.of_string("id")
    creation_date = Metadata.of_long("creationDate")
    commits_metadata = Metadata("commitsMetadata", CommitsMetadata)
    pass_reaper = Metadata.of_boolean("passReaper")
    number_of_security_update_dependabot = Metadata.of_long(
        "numberOfSecurityUpdateDependabo"
    )
    use_multiple_dependency_management_bots = Metadata.of_boolean(
        "use_multiple_dependency_management_bots"
    )
    build_system = Metadata.of_string("build_system")
    contains_package_json = Metadata.of_boolean("contains_package_json")
    stars = Metadata.of_integer("stars")
    is_fork = Metadata.of_boolean("is_fork")

    # Workflow Declaration and Execution
    workflow = (
        WorkflowBuilder()
        .input(
            Loader(
                url,
                creation_date,
                commits_metadata,
                pass_reaper,
                number_of_security_update_dependabot,
                use_multiple_dependency_management_bots,
                build_system,
                contains_package_json,
                stars,
                is_fork,
            )
        )
        # Filter project non-fork
        .filter_operator("is_fork == False")
        # Filter project with more than X stars
        .filter_operator("stars >= 50")  # adjust threshold
        # Filter project with a commit before June 1, 2019
        .filter_operator(
            "commits_metadata.get_first_commit_date() < date_to_epoch_day(2019, 6, 1)"
        )
        # Filter project with at least an update after June 1, 2019
        .filter_operator(
            "commits_metadata.get_total_commit() > commits_metadata.get_total_commit_at_date(1, 6, 2019)"
        )
        # Filter project with more than 100 commits before June 1, 2019
        .filter_operator("commits_metadata.get_total_commit_at_date(1, 6, 2019) > 100")
        # * Filter project with at least one commit for each month between June 1, 2019 and May 31, 2020
        .filter_operator(
            " and ".join(
                [
                    f"commits_metadata.get_number_of_commit_by_month({year}, {month}) > 0"
                    for year, month in months_between(2019, 6, 2020, 5)
                ]
            )
        )
        # * Filter project including package.json manifest at the root
        .filter_operator("contains_package_json == True")
        # * Filter project using Reaper
        .add_metadata(Loader(pass_reaper))
        .filter_operator("pass_reaper == True")
        # * Filter project having at least a dependabot security update targeting npm or yarn
        .filter_operator("number_of_security_update_dependabot > 0")
        # * Filter out projects that use multiple dependency management bots (Maven, RubyGem)
        .filter_operator("use_multiple_dependency_management_bots == False")
    )

    workflow.execute_workflow()


if __name__ == "__main__":
    main()
