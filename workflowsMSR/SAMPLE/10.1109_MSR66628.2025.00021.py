from pathlib import Path

from paper_extension.element.loader.CsvLoader import CsvLoader
from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# Enhancing Just-In-Time Defect Prediction Models with Developer-Centric Features.

# The datasets we used in our study are based on the datasets
# released by Tian et al. [41] [...] 18 projects they considered.
# [...]we excluded the commits
# (i) made before March 2015
# (ii) no longer available in the repository at the time we conducted our study.
# We excluded projects for which we did not have a sufficient number of commits.
# As a result, we considered six projects.


def main():
    input_path = Path("tian_dataset.json")
    number_of_commit_after_march_2015 = Metadata.of_integer(
        "number_of_commit_after_march_2015"
    )
    number_of_commit_still_available_on_github = Metadata.of_integer(
        "number_of_commit_still_available_on_github"
    )
    url = Metadata.of_string("url")

    # Workflow Declaration and Execution
    workflow = (
        WorkflowBuilder()
        .input(
            CsvLoader(
                input_path,
                url,
                number_of_commit_after_march_2015,
                number_of_commit_still_available_on_github,
            )
        )
        .filter_operator(
            "number_of_commit_still_available_on_github + number_of_commit_after_march_2015 > ???? "
        )
        .output(CsvWriter("out.csv"))
    )
    workflow.execute_workflow()


if __name__ == "__main__":
    main()
