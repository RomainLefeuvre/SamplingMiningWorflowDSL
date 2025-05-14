# CrashJS: A NodeJS Benchmark for Automated Crash Reproduction
# DOI : 10.1145/3643991.3644912
from newDSL.element.loader.LoaderFactory import LoaderFactory
from newDSL.element.writer.WritterFactory import WritterFactory
from newDSL.metadata.Metadata import Metadata
from newDSL.operator.OperatorFactory import OperatorFactory

# *Filter JavaScript as main language
# *Sort by number of stars
# -> : https://github.com/topics/javascript?l=javascript&o=desc&
# s=stars
#
# *Filter NodeJS projects
#
# *Search through issues :
#     filter to keep closed issues
#     Sort them by most recent
#
# *Manual verification of project and dependency versions

json_loader = LoaderFactory.json_loader
json_writer = WritterFactory.json_writer

filter_operator = OperatorFactory.filter_operator
manual_sampling_operator = OperatorFactory.manual_sampling_operator
systematic_selection_operator = OperatorFactory.systematic_selection_operator


def main():
    import os
    input_path = os.path.join(os.path.dirname(__file__), "input.json")

    language = Metadata.of_string("language")
    framework = Metadata.of_string("framework")
    nbStars = Metadata.of_string("nbStars")
    issues = Metadata.of_string("issues")

    cardinality = 42 # Ambiguous, should be the number of projects to sample ?

    # "Projects from this search that are client-side JavaScript
    # frameworks or tools, such as React, Vue, and Bootstrap were ex-
    # cluded as these projects are built to run on web browsers, rather
    # than Node.js."
    #   => filter to keep only NodeJS projects OR exclude others like they do ?

    # Do we retrieve the issues and then filter them ? Or only project sampling ?
    op = (
        filter_operator(language.bool_constraint(lambda x: x == "JS"))
        # Ambiguous, missing qualitative constraint to say we keep only NodeJS projects
        .chain(filter_operator(framework.bool_constraint(lambda x: x == "NodeJS")))
        .chain(manual_sampling_operator("Repo 1", "...", "Repo 23"))
        .chain(systematic_selection_operator(cardinality, nbStars, 1))
        .input(json_loader(input_path, language, framework, nbStars, issues))
        .output(json_writer("out.json"))
        .execute_workflow()
    )

    print(op)


if __name__ == "__main__":
    main()