from newDSL.metadata.Metadata import Metadata
from newDSL.operator.OperatorFactory import OperatorFactory
from newDSL.element.loader.LoaderFactory import LoaderFactory
from newDSL.element.writer.WritterFactory import WritterFactory

filter_operator = OperatorFactory.filter_operator
random_selection_operator = OperatorFactory.random_selection_operator

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
        filter_operator(language.bool_constraint(lambda x: x == "JavaScript"))
        .chain(random_selection_operator(10))
        .input(json_loader(input_path, id_, commit_nb, url, language))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)

if __name__ == "__main__":
    main()