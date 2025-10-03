from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.element.Loader import Loader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# ---- Metadata ----
url = Metadata.of_string("id")
language = Metadata.of_string("language")
stars = Metadata.of_integer("stars")
is_fork = Metadata.of_boolean("isFork")
commits = Metadata.of_integer("commits")
have_pr_js_security_created_by_dependabot = Metadata.of_boolean(
    "have_pr_js_security_created_by_dependabot"
)


def main():
    workflow = (
        WorkflowBuilder()
        # Start from GitHub loader
        .input(
            Loader(
                url,
                language,
                stars,
                is_fork,
                commits,
                have_pr_js_security_created_by_dependabot,
            )
        )
        # Keep projects with JS security PRs created by Dependabot
        .filter_operator("have_pr_js_security_created_by_dependabot")
        # Keep only JavaScript projects
        .filter_operator("language == 'JavaScript'")
        # Keep projects with more than X stars
        .filter_operator("stars > X")
        .filter_operator("not isFork")
        # Keep projects with more than 20 commits
        .filter_operator("commits > 20")
        # Output final dataset
        .output(CsvWriter("10.1109_MSR52588.2021.00037.csv"))
    )

    workflow.execute_workflow()
