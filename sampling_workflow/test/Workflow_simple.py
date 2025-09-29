from sampling_workflow.WorkflowBuilder import WorkflowBuilder
from sampling_workflow.exec_visualizer.WorkflowVisualizer import WorkflowVisualizer
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory
from sampling_workflow.Workflow import Workflow
from sampling_workflow.operator.OperatorBuilder import OperatorBuilder
from sampling_workflow.operator.OperatorFactory import OperatorFactory
from sampling_workflow.operator.clustering.SubWorkflowOperatorBuilder import (
    SubWorkflowOperatorBuilder,
)
from sampling_workflow.operator.selection.filter.FilterOperator import FilterOperator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer
filter_operator = SubWorkflowOperatorBuilder.filter_operator


def main():
    import os

    input_path = os.path.join(os.path.dirname(__file__), "input.json")

    url = Metadata.of_string("url")
    language = Metadata.of_string("language")
    id_ = Metadata.of_string("id")
    commit_nb = Metadata.of_integer("commitNb")
    year = Metadata.of_integer("year")

    w = (
        WorkflowBuilder()
        .input(json_loader(input_path, id_, commit_nb, language))
        .filter_operator("commitNb > 2000 and commitNb < 7000")
        .random_selection_operator(40)
        .output(json_writer("out.json"))
    )

    # w = (WorkflowBuilder()
    #      .input(json_loader(input_path, id_, commit_nb, url, language))
    #      .grouping_operator(
    #         filter_operator(commit_nb.is_greater_than(2000)).filter_operator(commit_nb.is_less_than(5000)),
    #         filter_operator(language.is_equal("JavaScript"))
    #      )
    #     .random_selection_operator(1)
    #     .output(json_writer("out.json"))
    # )

    # w = (
    #     Workflow()
    #     .input(json_loader(input_path, id_, commit_nb, url, language))
    #     .grouping_operator(
    #         Workflow()
    #         .filter_operator(commit_nb.is_greater_than(1000))
    #         .random_selection_operator(10)
    #     )
    #     .output(json_writer("out.json"))
    # )

    w.execute_workflow()
    # w.analyze_workflow(commit_nb)

    WorkflowVisualizer(w).generate_graph()

    print(w)


if __name__ == "__main__":
    main()

# .filter_operator(language.is_equal("JavaScript"))
# .manual_sampling_operator("8","62", "90")
