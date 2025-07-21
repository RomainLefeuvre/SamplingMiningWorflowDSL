
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory
from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WritterFactory import WritterFactory

filter_operator = OperatorFactory.filter_operator
random_selection_operator = OperatorFactory.random_selection_operator
grouping_operator = OperatorFactory.grouping_operator
manual_sampling_operator = OperatorFactory.manual_sampling_operator
interactive_manual_sampling_operator = OperatorFactory.interactive_manual_sampling_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

def main():
    input_path = "input.json"  # Adjust path as needed

    url = Metadata.of_string("url")
    lang = Metadata.of_string("language")
    id = Metadata.of_string("id")
    commit_nb = Metadata.of_double("commitNb")

    # # Cluster Operator
    # cluster_operator = (
    #     grouping_operator(
    #         filter_operator(commit_nb.bool_constraint(lambda x: x < 100)),
    #         filter_operator(commit_nb.bool_constraint(lambda x: 100 <= x < 1000)),
    #         filter_operator(commit_nb.bool_constraint(lambda x: x >= 1000))
    #     )
    #     .chain(random_selection_operator(2))
    #     .get_workflow_root_operator()
    #     .input(json_loader(input_path, id, commit_nb, url, lang))
    #     .output(json_writer("cluster.json"))
    #     .execute()
    # )
    #
    # # Stratified Random Operator
    # stratified_operator = (
    #     grouping_operator(
    #         filter_operator(commit_nb.bool_constraint(lambda x: x < 100))
    #         .chain(random_selection_operator(10)),
    #         filter_operator(commit_nb.bool_constraint(lambda x: 100 <= x < 1000))
    #         .chain(random_selection_operator(10)),
    #         filter_operator(commit_nb.bool_constraint(lambda x: x >= 1000))
    #         .chain(random_selection_operator(10))
    #     )
    #     .get_workflow_root_operator()
    #     .input(json_loader(input_path, id, commit_nb, url, lang))
    #     .output(json_writer("stratified_random.json"))
    #     .execute()
    # )

    # Quota Operator
    quota_operator = (
        grouping_operator(
            filter_operator(commit_nb.bool_constraint(lambda x: x < 100))
            .chain(interactive_manual_sampling_operator()),
            filter_operator(commit_nb.bool_constraint(lambda x: 100 <= x < 1000))
            .chain(interactive_manual_sampling_operator()),
            filter_operator(commit_nb.bool_constraint(lambda x: x >= 1000))
            .chain(interactive_manual_sampling_operator())
        )
        .get_workflow_root_operator()
        .input(json_loader(input_path, id, commit_nb, url, lang))
        .output(json_writer("quota.json"))
        .execute()
    )

    # print("--------------------------------------")
    # print("Cluster Operator")
    # print(cluster_operator)
    # print("--------------------------------------")

    print("--------------------------------------")
    print("Quota Operator")
    print(quota_operator)
    print("--------------------------------------")

    # print("--------------------------------------")
    # print("Stratified Operator")
    # print(stratified_operator)
    # print("--------------------------------------")

if __name__ == "__main__":
    main()