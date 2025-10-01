from sampling_workflow.Workflow import Workflow
from sampling_workflow.WorkflowBuilder import WorkflowBuilder
from sampling_workflow.element.Loader import Loader
from datetime import datetime

from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorBuilder import OperatorBuilder

# ---- Metadata ----
latest_commit_date = Metadata.ofDate("latest_commit_date")
author_nb = Metadata.ofInteger("author_Nb")

# ---- Loader ----

# ---- Workflow ----
workflow =  WorkflowBuilder() \
    .input(Loader("2024-05-16-history-hosting")) \
    .filter_operator(latest_commit_date.bool_constraint(lambda x: x > datetime(2023, 1, 1))) \
    .grouping_operator(
        # First stratum: projects with less than 5 authors
        WorkflowBuilder()
        .filter_operator("author_nb < 5"))\
        .random_selection_operator(10000),

        # Second stratum: projects with 5 or more authors
        WorkflowBuilder()\
        .filter_operator(author_nb.bool_constraint(lambda x: x >= 5))\
        .random_selection_operator(10000)
    )

# ---- Execute workflow ----
workflow.execute()