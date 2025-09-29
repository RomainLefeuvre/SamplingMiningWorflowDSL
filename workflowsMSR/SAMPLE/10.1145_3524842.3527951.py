from sampling_workflow.WorkflowBuilder import WorkflowBuilder
from sampling_workflow.element.JsonLoader import JsonLoader
from sampling_workflow.element.CsvWriter import CsvWriter
from sampling_workflow.Metadata import Metadata
from pathlib import Path

from sampling_workflow.element.Loader import Loader


def main():
    url = Metadata.of_string("id")

    workflow = (
        WorkflowBuilder()
        .input(
            Loader(
                url,
            )
        )
        .output(CsvWriter("rodrigues.csv"))
    )

    workflow.execute_workflow()
