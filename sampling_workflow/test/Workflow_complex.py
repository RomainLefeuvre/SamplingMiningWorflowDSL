from sampling_workflow.Workflow import Workflow
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory
from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    input_path = "input.json"  # Adjust path as needed

    url = Metadata.of_string("url")
    lang = Metadata.of_string("language")
    id = Metadata.of_string("id")
    commit_nb = Metadata.of_double("commitNb")

    # # Cluster Operator
    cluster_operator = (
        Workflow()
        .grouping_operator(
            Workflow().filter_operator(commit_nb.is_less_than(100)),
            Workflow().filter_operator(commit_nb.is_between(100, 1000)),
            Workflow().filter_operator(commit_nb.is_greater_or_equal_than(1000)),
        )
        .random_selection_operator(2)
        .input(json_loader(input_path, id, commit_nb, url, lang))
        .output(json_writer("cluster.json"))
        .execute_workflow()
    )

    # Stratified Random Operator
    stratified_operator = (
        Workflow()
        .grouping_operator(
            Workflow()
            .filter_operator(commit_nb.is_less_than(2000))
            .random_selection_operator(10),
            Workflow()
            .filter_operator(commit_nb.is_between(2000, 5000))
            .random_selection_operator(10),
            Workflow()
            .filter_operator(commit_nb.is_less_or_equal_than(5000))
            .random_selection_operator(10),
        )
        .input(json_loader(input_path, id, commit_nb, url, lang))
        .output(json_writer("stratified_random.json"))
        .execute_workflow()
    )

    # # Quota Operator
    quota_operator = (
        Workflow()
        .grouping_operator(
            Workflow()
            .filter_operator(commit_nb.is_less_than(100))
            .manual_sampling_operator("1", "33", "54", "76", "38"),
            Workflow()
            .filter_operator(commit_nb.is_between(100, 1000))
            .manual_sampling_operator("6", "15", "14"),
            Workflow()
            .filter_operator(commit_nb.is_greater_or_equal_than(1000))
            .manual_sampling_operator("53", "54", "2", "5"),
        )
        .input(json_loader(input_path, id, commit_nb, url, lang))
        .output(json_writer("quota.json"))
        .execute_workflow()
    )
    #
    print("--------------------------------------")
    print("Cluster Operator")
    print(cluster_operator)
    print("--------------------------------------")

    print("--------------------------------------")
    print("Stratified Operator")
    print(stratified_operator)
    print("--------------------------------------")

    print("--------------------------------------")
    print("Quota Operator")
    print(quota_operator)
    print("--------------------------------------")


if __name__ == "__main__":
    main()
