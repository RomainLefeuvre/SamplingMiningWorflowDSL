from pathlib import Path

from sampling_workflow.element.CsvWriter import CsvWriter
from sampling_workflow.element.JsonLoader import JsonLoader
from sampling_workflow.Metadata import Metadata

from sampling_workflow.WorkflowBuilder import WorkflowBuilder


def main():
    # ---- Metadata ----
    url = Metadata.of_string("id")
    workflow = (
        WorkflowBuilder()
        .input(
            JsonLoader(
                Path("android_time_machine.json"),
                url,
            )
        )
        .output(CsvWriter("out.csv"))
    )

    workflow.execute_workflow()
