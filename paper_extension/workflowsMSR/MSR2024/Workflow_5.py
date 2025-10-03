from sampling_workflow.element.writer.WritterFactory import WritterFactory

from sampling_workflow.element.loader.LoaderFactory import LoaderFactory
from sampling_workflow.metadata.Metadata import Metadata
from sampling_workflow.operator.OperatorFactory import OperatorFactory

# GitBug-Java: A Reproducible Benchmark of Recent Java Bugs
# DOI : 10.1145/3643991.3644884

# *Exclude projects without GitHub Action Workflows that execute tests
# -> locally executable open-source repositories
# on GitHub
#
# *Filter project with Java
# *Filter projects with >= 20 stars
# *Filter projects with < 200MB
# *Exclude archived projects

filter_operator = OperatorFactory.filter_operator

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer


def main():
    use_github_action_tests = Metadata.of_boolean("useGithubActionTests")
    language = Metadata.of_string("language")
    nb_stars = Metadata.of_integer("nbStars")
    size = Metadata.of_integer("size")
    is_archived = Metadata.of_boolean("isArchived")

    op = (
        filter_operator(use_github_action_tests.bool_constraint(lambda x: x))
        .chain(filter_operator(language.bool_constraint(lambda x: x == "Java")))
        .chain(filter_operator(nb_stars.bool_constraint(lambda x: x >= 20)))
        .chain(filter_operator(size.bool_constraint(lambda x: x < 200)))
        .chain(filter_operator(is_archived.bool_constraint(lambda x: not x)))
        .input(
            json_loader(
                "input.json",
                use_github_action_tests,
                language,
                nb_stars,
                size,
                is_archived,
            )
        )
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)
