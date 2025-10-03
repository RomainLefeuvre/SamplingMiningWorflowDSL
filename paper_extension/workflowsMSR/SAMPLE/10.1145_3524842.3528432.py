from pathlib import Path

from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.element.Loader import Loader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# Mining Code Review Data to Understand Waiting Times Between Acceptance and Merging: An Empirical Analysis.


def main():
    # --- Metadata declarations (shared) ---
    url = Metadata.of_string("id")
    code_reviews = Metadata.of_long("codeReviews")

    # --- Workflow 1: Gerrit dataset (use entire dataset) ---
    WorkflowBuilder().input(
        Loader(Path(url)).output(  # assuming Gerrit dataset in JSON
            CsvWriter("gerrit_out.csv")
        )
    )

    # --- Workflow 2: Phabricator dataset ---
    (
        WorkflowBuilder()
        .input(Loader(url, code_reviews))
        .filter_operator("codeReviews >= 10000")
        .output(CsvWriter("phabricator_out.csv"))
    )
