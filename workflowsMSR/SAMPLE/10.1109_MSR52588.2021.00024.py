from sampling_workflow.WorkflowBuilder import WorkflowBuilder
from sampling_workflow.element.JsonLoader import JsonLoader
from sampling_workflow.element.CsvWriter import CsvWriter
from sampling_workflow.Metadata import Metadata
from pathlib import Path





def main():

    # ---- Metadata ----
    url = Metadata.of_string("id")
    workflow = WorkflowBuilder().input(JsonLoader(
            Path("android_time_machine.json"),
            url,
        )).output(CsvWriter("out.csv"))
    
    workflow.execute_workflow()