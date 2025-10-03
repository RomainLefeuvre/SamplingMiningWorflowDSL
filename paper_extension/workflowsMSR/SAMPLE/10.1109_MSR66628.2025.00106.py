from pathlib import Path

from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.element.loader import JsonLoader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# Prompting in the Wild: An Empirical Study of Prompt Evolution in Software Repositories.

# 1.Start from Prompt Set, a refined dataset of prompt extracted from 20,598 projects. We consider the associated raw dataset composed of the different projects.
# 2. Project are filtered if they do not contains at least one prompts that satisfy:
# - non empty prompt
# - in english
# - do not contain non-ascii character
# - length > 15 character
# Dataset reduce to 18,692 repo
# 3. Filter project with at least 50 stars
# 4. Filter project with less than 10 contributors
# 5. Filter project with an active development period of at least 6 months


def main():
    input_path = Path("prompt_set.json")
    contributors_nb = Metadata.of_integer("contributors_nb")
    stars = Metadata.of_integer("stars")
    number_of_prompts_after_filtering = Metadata.of_integer(  # noqa: F841
        "number_of_prompts_after_filtering"
    )
    is_dev_active_in_6_months = Metadata.of_boolean("is_dev_active_in_6_months")
    url = Metadata.of_string("url")

    # Workflow Declaration and Execution
    workflow = (
        WorkflowBuilder()
        .input(
            JsonLoader(
                input_path, url, contributors_nb, stars, is_dev_active_in_6_months
            )
        )
        .filter_operator("number_of_prompts_after_filtering > 0")
        .filter_operator("contributors_nb >= 10")
        .filter_operator("stars >= 50")
        .filter_operator("is_dev_active_in_6_months == True")
        .output(CsvWriter("out.csv"))
    )
    workflow.execute_workflow()


if __name__ == "__main__":
    main()
