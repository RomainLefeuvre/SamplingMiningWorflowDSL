from sampling_workflow.WorkflowBuilder import WorkflowBuilder
from sampling_workflow.analysis.HistWorkflowAnalysis import HistWorkflowAnalysis
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory
from sampling_workflow.Workflow import Workflow

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

def main():
    import os
    input_path = os.path.join(os.path.dirname(__file__), "input.json")

    url = Metadata.of_string("url")
    language = Metadata.of_string("language")
    id_ = Metadata.of_string("id")
    commit_nb = Metadata.of_double("commitNb")

    w = (
        WorkflowBuilder()
        .input(json_loader(input_path, id_, language))
        .random_selection_operator(50)
        .filter_operator(language.is_equal("JavaScript"))
        .output(json_writer("out.json"))
    )
    #
    # w = (
    #     Workflow()
    #     .input(json_loader(input_path, id_, language))
    #     .filter_operator(language.is_equal("JavaScript"))
    #     .random_selection_operator(10)
    #     .output(json_writer("out.json"))
    #     .execute_workflow()
    # )

    w = (
        Workflow()
        .input(json_loader(input_path, id_, commit_nb, url, language))
        .grouping_operator(
            Workflow()
            .filter_operator(commit_nb.bool_constraint(lambda x: x > 1000))
            .random_selection_operator(10)
        )
        .output(json_writer("out.json"))
    )

    w.execute_workflow()
    w.analyze_workflow(language)
    print (w)

if __name__ == "__main__":
    main()

# .filter_operator(language.is_equal("JavaScript"))
# .manual_sampling_operator("8","62", "90")
