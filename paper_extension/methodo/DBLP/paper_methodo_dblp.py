from pathlib import Path
from typing import List
from paper_extension.element.loader.CsvLoader import CsvLoader
from sampling_workflow.WorkflowBuilder import WorkflowBuilder
from sampling_workflow.analysis.CoverageTest import CoverageTest
from sampling_workflow.analysis.HistWorkflowAnalysis import HistWorkflowAnalysis
from sampling_workflow.constraint.BoolConstraint import BoolConstraint
from sampling_workflow.exec_visualizer.WorkflowVisualizer import WorkflowVisualizer
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.element.loader.LoaderFactory import *
from sampling_workflow.element.writer.WriterFactory import *
from sampling_workflow.Workflow import Workflow
import os


def main():
    # Define the input path and metadata of DBLB dataset
    input_path =  Path("paper_extension/methodo/DBLP/msr.csv")
    title = Metadata.of_string("title")
    year = Metadata.of_integer("year")
    numPages = Metadata.of_integer("numPages")
    title = Metadata.of_string("title")
    doi = Metadata.of_string("DOI")

    # Define the IEEE dataset path and metadata
    IEEE_path =  Path("paper_extension/methodo/IEEE_DATA")
    iee_keyword_list = Metadata.of("IEEE Terms", list)
    author_keyword_list = Metadata.of("Author Keywords", list)

    # Workflow Declaration and Execution
    workflow = WorkflowBuilder().input(CsvLoader(input_path, doi, title,year,numPages))\
                                .filter_operator("2021 <= year <= 2025")\
                                .filter_operator("numPages > 6")\
                                .add_metadata(CsvLoader(IEEE_path, doi,iee_keyword_list,author_keyword_list))\
                                .random_selection_operator(cardinality=65,seed=4242)\
                                .output(JsonWriter("paper_extension/methodo/DBLP/out.json"))\

    # Workflow Execution
    workflow.execute_workflow()
    # Workflow Analysis
    HistWorkflowAnalysis(year,100,category=True,sort=False).analyze(workflow)
    HistWorkflowAnalysis(iee_keyword_list,top_x=50,category=True,sort=True).analyze(workflow)
    CoverageTest(iee_keyword_list,workflow.get_operator_by_position(1).get_output(),
                                  workflow.get_workflow_output()).compute_coverage(50)

    WorkflowVisualizer(workflow).generate_graph()
    print(workflow)

if __name__ == "__main__":
    main()


