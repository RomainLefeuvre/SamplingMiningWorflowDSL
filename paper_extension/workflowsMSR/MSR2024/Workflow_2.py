from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# An Investigation of Patch Porting Practices of the Linux Kernel Ecosystem
# DOI : 10.1145/3643991.3644902

interactive_manual_sampling_operator = (
    OperatorFactory.interactive_manual_sampling_operator
)

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

# Purposive sampling on OS repositories from LWN list


def main():
    op = (
        interactive_manual_sampling_operator()
        .input(json_loader("lwn_dist_list.json"))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
