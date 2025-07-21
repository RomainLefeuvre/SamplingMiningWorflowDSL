from pathlib import Path
from typing import List
from paper_extension.element.loader.CsvLoader import CsvLoader
from sampling_workflow.analysis.HistWorkflowAnalysis import HistWorkflowAnalysis
from sampling_workflow.constraint.BoolConstraint import BoolConstraint
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory
from sampling_workflow.Workflow import Workflow

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

def main():
    import os
    input_path =  Path("paper_extension/methodo/DBLP/msr.csv")
    title = Metadata.of_string("title")
    year = Metadata.of_integer("year")
    pages = Metadata.of_integer("numPages")
    title = Metadata.of_string("Document Title")
    doi = Metadata.of_string("doi")

    # Workflow Declaration and Execution
    w = (
        Workflow()
        .filter_operator(pages.is_greater_than(6))
        .filter_operator(year.is_greater_or_equal_than(2021))
        .filter_operator(year.is_less_or_equal_than(2025))
        .random_selection_operator(cardinality=63,seed=42)
        .input(CsvLoader(input_path, doi, title,year,pages))
        .output(json_writer("paper_extension/methodo/IEEE_DATA/out.json"))
        .execute_workflow()
    )
    print(w)

    HistWorkflowAnalysis(year,100).analyze(w)

if __name__ == "__main__":
    main()

# .filter_operator(language.is_equal("JavaScript"))
# .manual_sampling_operator("8","62", "90")
