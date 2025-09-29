from pathlib import Path

from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.element.loader import JsonLoader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# The Ecosystem of Open-Source Music Production Software - A Mining Study on the Development Practices of VST Plugins on GitHub.

# 1. select repositories whose topic contains 'VST'
# 2. duplicate removal
# 3. Manual analysis (check for inclusion and exclusion criteria)
#
# second sample of projects without VST
# 1. Filter for projects without VST plugins
# 2. Random sampling of 299 repos with the same distribution as the previous sample
# 3. Manual analysis (check for non-VST related exclusion criteria)


def main():
    input_path = Path("GitHub.json")
    topic = Metadata.of_string("topic")

    has_VST_plugin = Metadata.of_boolean("has_VST_plugin")
    url = Metadata.of_string("url")

    # Workflow Declaration and Execution
    workflow1 = (
        WorkflowBuilder()
        .input(JsonLoader(input_path, url, topic))
        .filter_operator("topic.contains('VST')")
        # Add a filter/operator to remove duplicates ?
        .manual_sampling_operator()
        .output(CsvWriter("out.csv"))
    )

    workflow1.execute_workflow()

    # Workflow Declaration and Execution
    workflow2 = (
        WorkflowBuilder()
        .input(JsonLoader(input_path, url, has_VST_plugin))
        .filter_operator("not has_VST_plugin")
        .random_selection_operator(
            299
        )  # how to get the same distribution as the previous sample?
        .manual_sampling_operator()
        .output(CsvWriter("out.csv"))
    )

    workflow2.execute_workflow()


if __name__ == "__main__":
    main()
