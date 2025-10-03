from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# PeaTMOSS: A Dataset and Initial Analysis of Pre-Trained Models in Open-Source Software
# DOI : 10.1145/3643991.3644907

# * Filter for public repos
# * Filter for non-forked
# * Filter for non-archived
# * Filter for >= 5 stars
# * Check for signature of PTM usage in apps

filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    # Les repos sont forcément publiques non ?

    is_public = Metadata.of_boolean("is_public")
    is_forked = Metadata.of_boolean("is_forked")
    is_archived = Metadata.of_boolean("is_archived")
    nb_stars = Metadata.of_integer("nbStars")
    has_ptm_signature = Metadata.of_boolean("hasPTMUsageSignature")

    op = (
        filter_operator(is_public.bool_constraint(lambda x: x))
        .chain(filter_operator(is_forked.bool_constraint(lambda x: not x)))
        .chain(filter_operator(is_archived.bool_constraint(lambda x: not x)))
        .chain(filter_operator(nb_stars.bool_constraint(lambda x: x >= 5)))
        .chain(filter_operator(has_ptm_signature.bool_constraint(lambda x: x)))
        .input(
            json_loader(
                "input.json",
                is_public,
                is_forked,
                is_archived,
                nb_stars,
                has_ptm_signature,
            )
        )
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
