from pathlib import Path

from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.element.Loader import Loader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# It Works (only) on My Machine: A Study on Reproducibility Smells in Ansible Scripts.

# 1. Sort repos by number of downloads
# 2. Filter repos with more than 10 scripts
# 3. Filter repos with 1 000 stars
# 4. Filter repos with 300 commits
# 5. Manual check if contains Ansible scripts
# 6. Include oci-ansible-collection dataset


def main():
    input_path = Path("ansible-galaxy.json")
    downloads_nb = Metadata.of_integer("downloads")
    scripts_nb = Metadata.of_integer("scripts_nb")
    stars_nb = Metadata.of_integer("stars")
    commits_nb = Metadata.of_integer("commits")

    url = Metadata.of_string("url")

    cardinality = 42  # Ambiguous

    # Workflow Declaration and Execution
    workflow = (
        WorkflowBuilder()
        .input(
            Loader(input_path, url, downloads_nb, scripts_nb, stars_nb, commits_nb)
        )
        .systematic_selection_operator(
            cardinality, downloads_nb, 1
        )  # Sort by downloads
        .filter_operator("scripts_nb > 10")  # Filter repos with more than 10 scripts
        .filter_operator("stars = 1000")  # Filter repos with more than 1000 stars
        .filter_operator("commits = 300")  # Filter repos with more than 300 commits
        .manual_sampling_operator()  # Manual check if contains Ansible scripts
        # Include oci-ansible-collection dataset
        .output(CsvWriter("out.csv"))
    )

    workflow.execute_workflow()


if __name__ == "__main__":
    main()
