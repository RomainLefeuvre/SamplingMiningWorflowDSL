from pathlib import Path

from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.element.loader import JsonLoader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# GIRT-Model: Automated Generation of Issue Report Templates.

# * Retrieve the GIRT-Data dataset


def main():
    input_path = Path("girt-dataset.json")
    url = Metadata.of_string("url")

    # Workflow Declaration and Execution
    workflow = (
        WorkflowBuilder()
        .input(JsonLoader(input_path, url))
        .output(CsvWriter("out.csv"))
    )

    workflow.execute_workflow()


if __name__ == "__main__":
    main()
