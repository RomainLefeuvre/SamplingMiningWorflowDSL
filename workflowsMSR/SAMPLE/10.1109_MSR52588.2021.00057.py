from sampling_workflow.element.CsvWriter import CsvWriter
from sampling_workflow.Metadata import Metadata

from sampling_workflow.element.Loader import Loader
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# ---- Metadata ----
url = Metadata.of_string("id")  # repository id
contain_correct_Dockerfile = Metadata.of_boolean("contain_correct_Dockerfile")


def main():
    workflow = (
        WorkflowBuilder()
        # Start from WOC distinct repositories
        .input(Loader(url, contain_correct_Dockerfile))
        # Keep only repositories containing a correct Dockerfile
        .filter_operator("contain_correct_Dockerfile")
        # Output the filtered repositories
        .output(CsvWriter("woc_repos_correct_dockerfile.csv"))
    )

    workflow.execute_workflow()
