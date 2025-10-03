

from sampling_workflow.element.Loader import Loader
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

url = Metadata.of_string("url")
language = Metadata.of_string("language")
creation_date = Metadata.of_long("creation_date")


def dataset1():
    return (
        WorkflowBuilder()
        .input(Loader(url, language, creation_date))
        # Filter Python projects
        .filter_operator("language == 'Python'")
        # Filter projects created after March 20, 2019
        .filter_operator("creation_date > date(2019, 3, 20)")
    )


def dataset2():
    return (
        WorkflowBuilder()
        .input(Loader(url, language, creation_date))
        # Filter Python projects
        .filter_operator("language == 'Python'")
        # Filter projects created after March 11, 2021
        .filter_operator("creation_date > date(2021, 3, 11)")
    )
