from newDSL2.Workflow import Workflow
from newDSL2.metadata.Metadata import Metadata
from newDSL2.operator.OperatorFactory import OperatorFactory
from newDSL2.element.loader.LoaderFactory import LoaderFactory
from newDSL2.element.writer.WritterFactory import WritterFactory

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

def main():
    input_path = "input.json"  # Adjust path as needed

    url = Metadata.of_string("url")
    lang = Metadata.of_string("language")
    id = Metadata.of_string("id")
    commit_nb = Metadata.of_double("commitNb")

    # Cluster Operator
    # cluster_operator = (
    #     Workflow()
    #     .grouping_operator(
    #         Workflow()
    #         .filter_operator(commit_nb.bool_constraint(lambda x: x < 100)),
    #         Workflow()
    #         .filter_operator(commit_nb.bool_constraint(lambda x: 100 <= x < 1000)),
    #         Workflow()
    #         .filter_operator(commit_nb.bool_constraint(lambda x: x >= 1000))
    #     )
    #     .random_selection_operator(2)
    #     .input(json_loader(input_path, id, commit_nb, url, lang))
    #     .output(json_writer("cluster.json"))
    #     .execute_workflow()
    #     .display()
    # )

    # Stratified Random Operator
    stratified_operator = (
        Workflow()
        .grouping_operator(
            Workflow()
            .filter_operator(commit_nb.bool_constraint(lambda x: x < 100))
            .random_selection_operator(10),
            Workflow()
            .filter_operator(commit_nb.bool_constraint(lambda x: 100 <= x < 1000))
            .random_selection_operator(10),
            Workflow()
            .filter_operator(commit_nb.bool_constraint(lambda x: x >= 1000))
            .random_selection_operator(10)
        )
        .input(json_loader(input_path, id, commit_nb, url, lang))
        .output(json_writer("stratified_random.json"))
        .execute_workflow()
        .display()
    )
    #
    # # Quota Operator
    # quota_operator = (
    #     grouping_operator(
    #         filter_operator(commit_nb.bool_constraint(lambda x: x < 100))
    #         .chain(manual_sampling_operator("1", "10", "54", "76", "38")),
    #         filter_operator(commit_nb.bool_constraint(lambda x: 100 <= x < 1000))
    #         .chain(manual_sampling_operator("6", "8", "14")),
    #         filter_operator(commit_nb.bool_constraint(lambda x: x >= 1000))
    #         .chain(manual_sampling_operator("53", "54", "2", "5"))
    #     )
    #     .get_workflow_root_operator()
    #     .input(json_loader(input_path, id, commit_nb, url, lang))
    #     .output(json_writer("quota.json"))
    #     .execute()
    # )

    # print("--------------------------------------")
    # print("Cluster Operator")
    # print(cluster_operator)
    # print("--------------------------------------")

    # print("--------------------------------------")
    # print("Quota Operator")
    # print(quota_operator)
    # print("--------------------------------------")
    #
    # print("--------------------------------------")
    # print("Stratified Operator")
    # print(stratified_operator)
    # print("--------------------------------------")

if __name__ == "__main__":
    main()