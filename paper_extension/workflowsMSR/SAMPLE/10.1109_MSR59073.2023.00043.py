from sampling_workflow.element.Loader import Loader
from sampling_workflow.element.loader.LoaderFactory import *
from sampling_workflow.element.writer.WriterFactory import *
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.WorkflowBuilder import WorkflowBuilder

# Unveiling the Relationship Between Continuous
# Integration and Code Coverage


# CI dataset :
# * Start from Nery et al dataset
# * Random sampling of 30  projects

# NO CI dataset:

# * Start from github
# * Filter the 3k most starred
# * Add data from travis CI
# * Filter project with no travis CI build
# * Filter project with at least four year of activity
# *  Add is a toy metadata (manually evaluated ?)
# * Add has a test metatadata (manually evaluated ?)
# * Filter project not a toy
#  * Filter project having test
#  Add metadata owner_confirm_no_CI
#     Filter project where author confirm that no_ci was present
# * Random sampling of 30 projects

creation_date = Metadata.of_long("creationDate")
has_activity = Metadata.of_boolean("has_activity")
stars = Metadata.of_integer("stars")
is_fork = Metadata.of_boolean("isFork")
url = Metadata.of_string("url")
has_travis_ci = Metadata.of_boolean("has_travis_ci")
is_toy = Metadata.of_boolean("is_toy")  # manually evaluated
has_test = Metadata.of_boolean("has_test")  # manually evaluated
owner_confirm_no_ci = Metadata.of_boolean("owner_confirm_no_ci")


workflow = (
    WorkflowBuilder()
    .input(
        Loader(
            url,
            creation_date,
            has_activity,
            stars,
            is_fork,
            has_travis_ci,
            is_toy,
            has_test,
            owner_confirm_no_ci,
        )
    )
    .systematic_selection_operator(3000, "stars", reverse=True)
    .add_metadata(Loader(url, has_travis_ci))
    .filter_operator("not has_travis_ci")
    .filter_operator("has_activity")
    .add_metadata(Loader(url, is_toy, has_test))
    .filter_operator("not is_toy and not has_test")
    .add_metadata(Loader(url, owner_confirm_no_ci))
    .random_selection_operator(cardinality=30, seed=42)
)
