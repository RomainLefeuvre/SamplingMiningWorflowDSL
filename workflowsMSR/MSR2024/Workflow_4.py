from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.element.writer.WriterFactory import WritterFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# Fine-Grained Just-In-Time Defect Prediction at the Block Level in Infrastructure-as-Code (IaC)
# DOI : 10.1145/3643991.3644934

# *Filter repositories containing a terraform file
# (Partial metadata, only on a subset of element)
#
# *Filter out archived repo
#
# *FIlter out non starred,unlicensed
#
# * Add a new metadata "Is an educational repo" --> Manual evaluation --> could be also described as purposive sampling
#
# *excluded provider repo dev by hasicorp
#
# *Filter monthly commit >= 7.0
# *Filter >= 2 contributors, with a combined number of commits must constitute >= 80% of overall contributions
# *Filter with >= 1 push events in the last 6 months
#
# *Filter with >= 11% of the project files must consist of IaC scripts
#
# *Filter projects with >= 300 modified blocs (amoug various commits)
# *Filter with >= 5% of defects in its changed blocks
# *Filter with >= 3 defective blocks in the last 6 months

filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    use_terraform = Metadata.of_boolean("use_terraform")
    is_archived = Metadata.of_boolean("is_archived")
    is_starred = Metadata.of_boolean("is_starred")
    is_licensed = Metadata.of_boolean("is_licensed")
    dev_company = Metadata.of_string("dev_company")

    average_monthly_commit = Metadata.of_double("average_monthly_commit")
    nb_contributer = Metadata.of_integer("nb_contributer")
    nb_push_event = Metadata.of_integer("nb_push_event")

    iac_ratio = Metadata.of_double("iac_ratio")
    modified_blocs = Metadata.of_integer("modified_blocs")
    defect_ratio = Metadata.of_double("defect_ratio")
    defective_blocs = Metadata.of_integer("defective_blocs")

    # "excluded those designed
    # for educational courses, labs, or workshops"
    # -> purposive sampling ?
    # one metadata to say it's not a garbage/useless educational repos

    op = (
        filter_operator(use_terraform.bool_constraint(lambda x: x))
        .chain(filter_operator(is_archived.bool_constraint(lambda x: not x)))
        .chain(filter_operator(is_starred.bool_constraint(lambda x: x)))
        .chain(filter_operator(is_licensed.bool_constraint(lambda x: x)))
        .chain(filter_operator(dev_company.bool_constraint(lambda x: x != "HashiCorp")))
        .chain(
            filter_operator(average_monthly_commit.bool_constraint(lambda x: x >= 7.0))
        )
        .chain(filter_operator(nb_contributer.bool_constraint(lambda x: x >= 2)))
        .chain(filter_operator(nb_push_event.bool_constraint(lambda x: x >= 1)))
        .chain(filter_operator(iac_ratio.bool_constraint(lambda x: x >= 0.11)))
        .chain(filter_operator(modified_blocs.bool_constraint(lambda x: x >= 300)))
        .chain(filter_operator(defect_ratio.bool_constraint(lambda x: x >= 0.05)))
        .chain(filter_operator(defective_blocs.bool_constraint(lambda x: x >= 3)))
        .input(
            json_loader(
                "input.json",
                use_terraform,
                is_archived,
                is_starred,
                is_licensed,
                dev_company,
                average_monthly_commit,
                nb_contributer,
                nb_push_event,
                iac_ratio,
                modified_blocs,
                defect_ratio,
                defective_blocs,
            )
        )
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
