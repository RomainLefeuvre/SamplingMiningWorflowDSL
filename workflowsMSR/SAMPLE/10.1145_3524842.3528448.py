from sampling_workflow.element.Loader import Loader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# Do Small Code Changes Merge Faster? A Multi-Language Empirical Investigation.
# * start from github
# * filter project using one of the following language (C,
# C++, C#, Java, JavaScript, PHP, Python, Ruby, Shell, and TypeScript.)
# * systematic selection  100 most forked project
# * partition by language
# * systematic selection 10 project,  descending based on number of merged pull request


# ---- Metadata declarations ----
url = Metadata.of_string("id")
language = Metadata.of_string("language")
forks = Metadata.of_integer("forks")
merged_pull_requests = Metadata.of_integer("merged_pull_requests")

LANGS = [
    "C",
    "C++",
    "C#",
    "Java",
    "JavaScript",
    "PHP",
    "Python",
    "Ruby",
    "Shell",
    "TypeScript",
]

# ---- Workflow ----
workflow = (
    WorkflowBuilder()
    # start from github dataset
    .input(Loader(url, language, forks, merged_pull_requests))
    # filter projects using one of the specified languages
    .filter_operator(f"language in {LANGS!r}")
    # systematic selection: top 100 most forked (descending)
    .systematic_selection_operator(cardinality=100, metadata_name="forks", reverse=True)
    # partition by language, then select 10 most merged PRs per language
    .grouping_operator(
        *[
            WorkflowBuilder()
            .filter_operator(f"language == '{lang}'")
            .systematic_selection_operator(
                cardinality=10, metadata_name="mergedPullRequests", reverse=True
            )
            for lang in LANGS
        ]
    )
)

workflow.execute_workflow()
