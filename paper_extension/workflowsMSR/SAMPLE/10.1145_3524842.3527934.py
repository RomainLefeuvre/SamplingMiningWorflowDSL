from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.element.Loader import Loader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# Methods for Stabilizing Models Across Large Samples of Projects (with case studies on Predicting Defect and Project Health).
# * Start from github
# * filter project with at least one pull request
# * filter project with more than 20 commits
# * filter project with at least 50 weeks of developement activity
# * filter project with more than 10 issues
# * filter project with at least 10 contributors
# * filter project with at least 10 defective commit
# * filter out project that are forks


def main():
    # --- Metadata declarations ---
    url = Metadata.of_string("id")
    pull_requests = Metadata.of_long("pullRequests")
    commits = Metadata.of_long("commits")
    weeks_of_activity = Metadata.of_long("weeksOfActivity")
    issues = Metadata.of_long("issues")
    contributors = Metadata.of_long("contributors")
    defective_commits = Metadata.of_long("defective_commits")
    is_fork = Metadata.of_boolean("isFork")

    # --- Workflow ---
    (
        WorkflowBuilder()
        .input(
            Loader(
                url,
                pull_requests,
                commits,
                weeks_of_activity,
                issues,
                contributors,
                defective_commits,
                is_fork,
            )
        )
        .filter_operator("pullRequests > 0")
        .filter_operator("commits > 20")
        .filter_operator("weeksOfActivity >= 50")
        .filter_operator("issues > 10")
        .filter_operator("contributors >= 10")
        .filter_operator("defective_commits >= 10")
        .filter_operator("not isFork ")
        .output(CsvWriter("github_filtered.csv"))
    )
