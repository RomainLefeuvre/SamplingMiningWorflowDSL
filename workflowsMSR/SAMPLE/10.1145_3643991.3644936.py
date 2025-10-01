from pathlib import Path

from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.element.loader import JsonLoader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# GuiEvo: Automated Evolution of Mobile Application GUIs.
# * Filter on F-Droid for apps with source code available on GitHub
# * Filter apps with more than 1000 downloads on Playstore


def main():
    input_path = Path("input.json")
    url = Metadata.of_string("url")
    is_code_available_on_github = Metadata.of_boolean("is_code_available_on_github")  # noqa: F841
    nb_downloads = Metadata.of_integer("nb_downloads")  # noqa: F841

    # Workflow Declaration and Execution
    workflow = (
        WorkflowBuilder()
        .input(JsonLoader(input_path, url))
        .filter_operator("is_code_available_on_github")
        .filter_operator("nb_downloads >= 1000")
        .output(CsvWriter("out.csv"))
    )

    workflow.execute_workflow()


if __name__ == "__main__":
    main()
