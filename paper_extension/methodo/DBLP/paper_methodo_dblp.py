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
    title = Metadata.of_string("title")
    doi = Metadata.of_string("DOI")

    IEEE_path =  Path("paper_extension/methodo/IEEE_DATA")
    iee_keyword_list = Metadata.of("IEEE Terms", list)
    author_keyword_list = Metadata.of("Author Keywords", list)

    # Workflow Declaration and Execution
    w = (
        Workflow()
        .input(CsvLoader(input_path, doi, title,year,pages))
        .filter_operator(year.is_between(2021, 2025))
        .filter_operator(pages.is_greater_than(6))
        .add_metadata(CsvLoader(IEEE_path, doi,iee_keyword_list,author_keyword_list))
        .random_selection_operator(cardinality=65,seed=42)
        .output(json_writer("paper_extension/methodo/DBLP/out.json"))
        .execute_workflow()
    )
    print(w)

    #HistWorkflowAnalysis(year,100,category=True,sort=False).analyze(w)
    HistWorkflowAnalysis(iee_keyword_list,top_x=10,category=True,sort=True).analyze(w)



if __name__ == "__main__":
    main()

# .filter_operator(language.is_equal("JavaScript"))
# .manual_sampling_operator("8","62", "90")
