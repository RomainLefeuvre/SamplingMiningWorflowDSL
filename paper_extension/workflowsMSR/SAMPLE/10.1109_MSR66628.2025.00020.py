from pathlib import Path

from paper_extension.element.loader.CsvLoader import CsvLoader
from paper_extension.element.writter.CsvWriter import CsvWriter
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# It's About Time: An Empirical Study of Date and Time Bugs in Open-Source Python Software..
# 1. Filter repo created after 2014
# 2. Filter repo that have over 100 stars
# 55k repos
# 3. purposive sampling : select repository using
# Datetime, Arrow, or Pendulum
# result in 22,132


def main():
    input_path = Path("tian_dataset.json")
    creation_date = Metadata.of_integer("creation_date")
    stars = Metadata.of_integer("stars")
    libraries = Metadata.of("libraries", set)
    url = Metadata.of_string("url")

    # Workflow Declaration and Execution
    workflow = (
        WorkflowBuilder()
        .input(CsvLoader(input_path, url, creation_date, stars, libraries))
        .filter_operator("creation_date >2014")
        .filter_operator("stars > 100")
        .filter_operator(
            "len(libraries.intersection(set(['Datetime', 'Arrow', 'Pendulum']))>0"
        )
        .output(CsvWriter("out.csv"))
    )
    workflow.execute_workflow()


if __name__ == "__main__":
    main()
