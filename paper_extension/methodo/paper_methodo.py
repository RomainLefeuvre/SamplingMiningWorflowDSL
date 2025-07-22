from pathlib import Path
from typing import List
from paper_extension.element.loader.CsvLoader import CsvLoader
from sampling_workflow.analysis.HistWorkflowAnalysis import HistWorkflowAnalysis
from sampling_workflow.constraint.BoolConstraint import BoolConstraint
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory
from sampling_workflow.Workflow import Workflow
import os

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

def main():
    input_path =  Path("paper_extension/methodo/IEEE_DATA")
    authors = Metadata.of_string("Authors")
    title = Metadata.of_string("Document Title")
    year = Metadata.of_integer("Publication Year")
    start_page = Metadata.of_integer("Start Page")
    end_page = Metadata.of_integer("End Page")
    iee_keyword_list = Metadata.of("IEEE Terms", list)
    author_keyword_list = Metadata.of("Author Keywords", list)
    id_ = Metadata.of_string("DOI")

    # Workflow Declaration and Execution
    w = (
        Workflow()
        .input(CsvLoader(input_path, id_, title,year,start_page,end_page,iee_keyword_list,author_keyword_list,authors))
        .filter_operator(year.is_greater_or_equal_than(2021))
        .filter_operator(year.is_less_or_equal_than(2025))
        .filter_operator(BoolConstraint(None,lambda start_page,end_page : (end_page-start_page+1) > 6, start_page,end_page))
        .random_selection_operator(65,2)
        .output(json_writer("paper_extension/methodo/IEEE_DATA/out.json"))
        .execute_workflow()
    )
    print(w)

    #HistWorkflowAnalysis(iee_keyword_list,5).analyze(w)
    #HistWorkflowAnalysis(year,20).analyze(w)


if __name__ == "__main__":
    main()


