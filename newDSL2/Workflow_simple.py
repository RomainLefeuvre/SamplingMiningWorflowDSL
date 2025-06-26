from newDSL2.metadata.Metadata import Metadata
from newDSL2.operator.OperatorFactory import OperatorFactory
from newDSL2.element.loader.LoaderFactory import LoaderFactory
from newDSL2.element.writer.WritterFactory import WritterFactory
from newDSL2.Workflow import Workflow

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

def main():
    import os
    input_path = os.path.join(os.path.dirname(__file__), "input.json")

    url = Metadata.of_string("url")
    language = Metadata.of_string("language")
    id_ = Metadata.of_string("id")
    commit_nb = Metadata.of_double("commitNb")

    # Workflow Declaration and Execution
    op = (
        Workflow()
        # .filter_operator(language.is_equal("JavaScript"))
        .filter_operator(commit_nb.is_more_than(5000))
        .random_selection_operator(10)
        # .manual_sampling_operator("8","62", "90")
        .input(json_loader(input_path, id_, commit_nb, url, language))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print (op)

if __name__ == "__main__":
    main()